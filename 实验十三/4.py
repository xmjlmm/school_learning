import cv2
import numpy as np
import time
from datetime import datetime
import os

class ZebraCrossingDetector:
    def __init__(self, debug=False):
        self.debug = debug
        self.detection_history = []
        self.evaluation_results = {
            'true_positives': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'total_frames': 0
        }
        
    def preprocess_image(self, img):
        """
        图像预处理 - 增强斑马线特征[1,3](@ref)
        """
        # 转换为HSV颜色空间，更好地处理光照变化[2](@ref)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 使用亮度通道(Value)而不是蓝色通道
        gray = hsv[:, :, 2].copy()
        
        # 自适应直方图均衡化 - 增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # 中值滤波去噪 - 保留边缘同时去除噪声[4](@ref)
        gray = cv2.medianBlur(gray, 5)
        
        # 自适应阈值处理 - 替代全局阈值[1](@ref)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        return thresh
    
    def detect_edges(self, processed_img):
        """
        边缘检测 - 使用Canny算法[1,4](@ref)
        """
        # Canny边缘检测
        edges = cv2.Canny(processed_img, 50, 150, apertureSize=3)
        return edges
    
    def calculate_gradient(self, edges):
        """
        计算梯度幅度和方向[4](@ref)
        """
        # 计算x轴和y轴的sobel因子
        sobelx = cv2.Sobel(edges, cv2.CV_32F, 1, 0, ksize=3)
        sobely = cv2.Sobel(edges, cv2.CV_32F, 0, 1, ksize=3)
        
        # 计算梯度和方向
        theta = np.arctan2(np.abs(sobely), np.abs(sobelx + 1e-10)) * 180 / np.pi
        amplitude = np.sqrt(sobelx**2 + sobely**2)
        
        # 过滤梯度太小的点
        mask = (amplitude > 30).astype(np.float32)
        amplitude = amplitude * mask
        
        return amplitude, theta
    
    def detect_by_texture(self, img, amplitude, theta):
        """
        基于纹理特征的斑马线检测[4](@ref)
        """
        zebra_lines = []
        
        # 斑马线纹理特征：梯度方向一致性高
        mask = (amplitude > 25).astype(bool)
        if np.sum(mask) > 0:
            # 计算梯度方向直方图
            h, b = np.histogram(theta[mask.astype(bool)], bins=range(0, 80, 5))
            
            # 找到主要方向
            main_direction_idx = h.argmax()
            low, high = b[main_direction_idx], b[main_direction_idx + 1]
            
            # 创建方向掩码
            direction_mask = ((theta >= low) & (theta <= high) & (amplitude > 25)).astype(np.float32)
            
            # 统计有效像素数量
            value = np.sum(amplitude * direction_mask > 0)
            
            # 斑马线应该有大量方向一致的边缘
            if value > 1500:  # 阈值可根据实际情况调整[4](@ref)
                # 查找轮廓
                contours, _ = cv2.findContours(direction_mask.astype(np.uint8), 
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) < 500:
                        continue
                    
                    # 获取边界矩形
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # 斑马线特征：长宽比大，水平方向延伸[4](@ref)
                    aspect_ratio = w / h
                    if aspect_ratio > 3 and w > 100:
                        zebra_lines.append((x, y, w, h))
                        
                        if self.debug:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return zebra_lines, img
    
    def detect_by_contours(self, processed_img, original_img):
        """
        基于轮廓分析的斑马线检测[1,3](@ref)
        """
        # 查找轮廓
        contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        zebra_lines = []
        
        for contour in contours:
            # 过滤小面积区域
            if cv2.contourArea(contour) < 500:
                continue
                
            # 获取边界矩形
            x, y, w, h = cv2.boundingRect(contour)
            
            # 斑马线特征：长宽比大，水平方向延伸[4](@ref)
            aspect_ratio = w / h
            if aspect_ratio > 3 and w > 100 and h < 50:
                zebra_lines.append((x, y, w, h))
                
                if self.debug:
                    cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return zebra_lines, original_img
    
    def detect_by_hough_lines(self, edges, original_img):
        """
        基于霍夫直线变换的斑马线检测[6](@ref)
        """
        # 霍夫直线检测
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=100, maxLineGap=50)
        
        zebra_lines = []
        
        if lines is not None:
            # 筛选近似水平的直线
            horizontal_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                if abs(angle) < 30 or abs(angle) > 150:  # 近似水平线
                    horizontal_lines.append(line[0])
            
            # 检查是否有多条平行线（斑马线特征）
            if len(horizontal_lines) >= 4:  # 至少4条线才可能是斑马线
                # 按y坐标排序
                lines_sorted = sorted(horizontal_lines, key=lambda x: x[1])
                
                # 计算间距均匀性
                spacings = []
                for i in range(1, len(lines_sorted)):
                    spacing = abs(lines_sorted[i][1] - lines_sorted[i-1][1])
                    spacings.append(spacing)
                
                # 检查间距的均匀性（斑马线间距应相对均匀）
                if len(spacings) > 2:
                    avg_spacing = np.mean(spacings)
                    std_spacing = np.std(spacings)
                    
                    # 间距相对均匀，可能是斑马线
                    if std_spacing < avg_spacing * 0.5:  # 标准差小于平均间距的一半
                        # 计算边界框
                        y_coords = [line[1] for line in lines_sorted] + [line[3] for line in lines_sorted]
                        x_coords = [line[0] for line in lines_sorted] + [line[2] for line in lines_sorted]
                        
                        y_min, y_max = min(y_coords), max(y_coords)
                        x_min, x_max = min(x_coords), max(x_coords)
                        
                        zebra_lines.append((x_min, y_min, x_max - x_min, y_max - y_min))
                        
                        if self.debug:
                            cv2.rectangle(original_img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        
        return zebra_lines, original_img
    
    def detect_zebra_crossing(self, img):
        """
        综合多种方法的斑马线检测
        """
        # 方法1: 预处理
        processed = self.preprocess_image(img)
        
        # 方法2: 边缘检测
        edges = self.detect_edges(processed)
        
        # 方法3: 梯度计算
        amplitude, theta = self.calculate_gradient(edges)
        
        # 尝试多种检测方法
        results = []
        
        # 方法A: 基于纹理特征
        zebra_texture, img_texture = self.detect_by_texture(img.copy(), amplitude, theta)
        results.extend(zebra_texture)
        
        # 方法B: 基于轮廓分析
        zebra_contours, img_contours = self.detect_by_contours(processed, img.copy())
        results.extend(zebra_contours)
        
        # 方法C: 基于霍夫直线
        zebra_hough, img_hough = self.detect_by_hough_lines(edges, img.copy())
        results.extend(zebra_hough)
        
        # 合并结果（简单的非极大值抑制）
        final_zebra_lines = self.non_max_suppression(results)
        
        return final_zebra_lines, img
    
    def non_max_suppression(self, boxes, overlap_thresh=0.5):
        """
        非极大值抑制 - 合并重叠的检测框[4](@ref)
        """
        if len(boxes) == 0:
            return []
        
        # 转换格式: (x, y, w, h) -> (x1, y1, x2, y2)
        boxes = np.array([(x, y, x + w, y + h) for x, y, w, h in boxes])
        pick = []
        
        # 获取坐标
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        
        # 计算面积
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)
        
        while len(idxs) > 0:
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            
            # 找到相交区域的坐标
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])
            
            # 计算相交区域的宽高和面积
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            overlap = (w * h) / area[idxs[:last]]
            
            # 删除重叠度高的框
            idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
        
        # 返回合并后的结果
        return [boxes[i].tolist() for i in pick]
    
    def calculate_metrics(self, detected, ground_truth):
        """计算评估指标"""
        self.evaluation_results['total_frames'] += 1
        
        if detected and ground_truth:
            self.evaluation_results['true_positives'] += 1
            return "TP"
        elif detected and not ground_truth:
            self.evaluation_results['false_positives'] += 1
            return "FP"
        elif not detected and ground_truth:
            self.evaluation_results['false_negatives'] += 1
            return "FN"
        else:
            return "TN"
    
    def get_performance_report(self):
        """生成性能报告"""
        tp = self.evaluation_results['true_positives']
        fp = self.evaluation_results['false_positives']
        fn = self.evaluation_results['false_negatives']
        total = self.evaluation_results['total_frames']
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + (total - tp - fp - fn)) / total if total > 0 else 0
        
        report = {
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1_score, 3),
            'accuracy': round(accuracy, 3),
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'total_frames': total
        }
        
        return report
    
    def visualize_detection(self, frame, zebra_lines, result):
        """可视化检测结果"""
        display_frame = frame.copy()
        
        # 绘制检测到的斑马线
        for x, y, w, h in zebra_lines:
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(display_frame, 'Zebra Crossing', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 添加性能信息
        cv2.putText(display_frame, f'Detection: {result}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return display_frame
    
    def process_video(self, video_path, ground_truth_callback=None):
        """处理视频流"""
        # 检查文件是否存在
        if not os.path.exists(video_path):
            print(f"错误：视频文件不存在于路径 '{video_path}'")
            return self.get_performance_report()
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"错误：无法打开视频文件 '{video_path}'")
            return self.get_performance_report()
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # 检测斑马线
            zebra_lines, processed_frame = self.detect_zebra_crossing(frame)
            
            # 评估检测结果
            ground_truth = ground_truth_callback(frame_count) if ground_truth_callback else False
            detected = len(zebra_lines) > 0
            result = self.calculate_metrics(detected, ground_truth)
            
            # 可视化结果
            display_frame = self.visualize_detection(processed_frame, zebra_lines, result)
            
            # 显示结果
            cv2.imshow('Zebra Crossing Detection', display_frame)
            
            # 每30帧打印一次性能报告
            if frame_count % 30 == 0:
                report = self.get_performance_report()
                print(f"\n帧 {frame_count} 性能报告:")
                for key, value in report.items():
                    print(f"{key}: {value}")
            
            # 退出条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("用户请求中断处理...")
                break
        
        # 清理资源
        cap.release()
        cv2.destroyAllWindows()
        
        # 生成最终报告
        end_time = time.time()
        processing_time = end_time - start_time
        fps = frame_count / processing_time if processing_time > 0 else 0
        
        final_report = self.get_performance_report()
        final_report['processing_fps'] = round(fps, 2)
        final_report['total_processing_time'] = round(processing_time, 2)
        final_report['processed_frames'] = frame_count
        
        print("\n" + "="*50)
        print("最终性能报告")
        print("="*50)
        for key, value in final_report.items():
            print(f"{key}: {value}")
        
        return final_report

# 使用示例
if __name__ == "__main__":
    # 初始化检测器
    detector = ZebraCrossingDetector(debug=True)
    
    # 简单的真实标签生成函数
    def simple_ground_truth(frame_number):
        # 示例：在第10-20帧和第50-60帧有斑马线
        if (10 <= frame_number <= 20) or (50 <= frame_number <= 60):
            return True
        return False
    
    # 处理视频
    video_path = "F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4"  # 替换为你的视频路径
    
    if not os.path.exists(video_path):
        print(f"错误：请确保视频文件存在于此路径：{video_path}")
    else:
        report = detector.process_video(video_path, simple_ground_truth)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"zebra_detection_report_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("斑马线检测报告\n")
            f.write("=" * 40 + "\n")
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
        
        print(f"\n报告已保存至: {report_filename}")