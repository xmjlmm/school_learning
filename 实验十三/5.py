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
        图像预处理 - 特别增强白色区域检测[1,3](@ref)
        """
        # 转换为HSV颜色空间，更好地分离白色区域[1](@ref)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 定义白色范围在HSV空间中的阈值
        lower_white = np.array([0, 0, 200])    # 低阈值：低饱和度，高亮度
        upper_white = np.array([180, 30, 255]) # 高阈值
        
        # 创建白色掩码
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # 应用中值滤波去噪[2,3](@ref)
        white_mask = cv2.medianBlur(white_mask, 5)
        
        return white_mask
    
    def enhance_white_regions(self, img):
        """
        增强白色区域 - 特别针对斑马线的白色条纹[1](@ref)
        """
        # 转换为LAB颜色空间，更好地处理亮度
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # 对亮度通道进行CLAHE增强
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        
        # 合并通道并转换回BGR
        enhanced_lab = cv2.merge([l_channel, a_channel, b_channel])
        enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        return enhanced_img
    
    def detect_edges(self, processed_img):
        """
        边缘检测 - 使用Canny算法[1,3](@ref)
        """
        # 应用形态学操作增强边缘
        kernel = np.ones((3, 3), np.uint8)
        processed_img = cv2.morphologyEx(processed_img, cv2.MORPH_CLOSE, kernel)
        processed_img = cv2.morphologyEx(processed_img, cv2.MORPH_OPEN, kernel)
        
        # Canny边缘检测
        edges = cv2.Canny(processed_img, 50, 150, apertureSize=3)
        return edges
    
    def detect_by_white_regions(self, img):
        """
        基于白色区域特征的斑马线检测[1](@ref)
        """
        # 增强白色区域
        enhanced_img = self.enhance_white_regions(img)
        
        # 预处理图像以突出白色区域
        white_mask = self.preprocess_image(enhanced_img)
        
        # 查找轮廓
        contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        zebra_lines = []
        
        for contour in contours:
            # 过滤小面积区域
            area = cv2.contourArea(contour)
            if area < 500 or area > 10000:  # 斑马线条纹不应太大或太小
                continue
                
            # 获取边界矩形
            x, y, w, h = cv2.boundingRect(contour)
            
            # 斑马线特征1: 长宽比大（水平方向的白色条纹）
            aspect_ratio = w / h
            if aspect_ratio < 2:  # 斑马线条纹应该是长条形的
                continue
                
            # 斑马线特征2: 白色区域应占据矩形大部分面积
            roi_mask = white_mask[y:y+h, x:x+w]
            white_ratio = np.sum(roi_mask > 0) / (w * h)
            if white_ratio < 0.6:  # 白色区域应占大部分
                continue
                
            # 斑马线特征3: 位置通常在地面区域
            height, width = img.shape[:2]
            if y < height * 0.2 or y > height * 0.8:  # 斑马线通常在中下部
                continue
                
            zebra_lines.append((x, y, w, h))
            
            if self.debug:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(img, f'WR:{white_ratio:.2f}', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return zebra_lines, img
    
    def detect_by_shape_features(self, white_mask, original_img):
        """
        基于形状特征的斑马线检测[3,6](@ref)
        """
        # 应用形态学操作连接相邻的白色区域
        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        zebra_lines = []
        
        for contour in contours:
            # 过滤小面积区域
            area = cv2.contourArea(contour)
            if area < 1000:  # 斑马线应该有较大面积
                continue
                
            # 获取边界矩形
            x, y, w, h = cv2.boundingRect(contour)
            
            # 形状特征1: 矩形度（轮廓面积与边界矩形面积之比）
            rect_area = w * h
            extent = area / rect_area if rect_area > 0 else 0
            if extent < 0.6:  # 斑马线应较为矩形
                continue
                
            # 形状特征2: 长宽比
            aspect_ratio = w / h
            if aspect_ratio < 3:  # 斑马线应该是长条形的
                continue
                
            # 形状特征3: 白色像素密度
            roi_mask = white_mask[y:y+h, x:x+w]
            white_density = np.sum(roi_mask > 0) / (w * h)
            if white_density < 0.4:  # 应有足够的白色像素
                continue
                
            zebra_lines.append((x, y, w, h))
            
            if self.debug:
                cv2.rectangle(original_img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(original_img, f'AR:{aspect_ratio:.1f}', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        return zebra_lines, original_img
    
    def detect_by_pattern(self, img, white_mask):
        """
        基于图案特征的斑马线检测（黑白相间模式）[1](@ref)
        """
        # 边缘检测
        edges = self.detect_edges(white_mask)
        
        # 霍夫直线检测[1](@ref)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=100, maxLineGap=30)
        
        zebra_lines = []
        
        if lines is not None and len(lines) >= 4:  # 斑马线应有多条线
            # 筛选近似水平的直线
            horizontal_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                if abs(angle) < 30 or abs(angle) > 150:  # 近似水平线
                    horizontal_lines.append(line[0])
            
            if len(horizontal_lines) >= 4:
                # 按y坐标排序并计算间距
                lines_sorted = sorted(horizontal_lines, key=lambda x: x[1])
                spacings = []
                for i in range(1, len(lines_sorted)):
                    spacing = abs(lines_sorted[i][1] - lines_sorted[i-1][1])
                    spacings.append(spacing)
                
                # 检查间距的均匀性（斑马线特征）
                if len(spacings) > 2:
                    avg_spacing = np.mean(spacings)
                    std_spacing = np.std(spacings)
                    
                    if std_spacing < avg_spacing * 0.5:  # 间距应相对均匀
                        # 计算整体边界框
                        y_coords = [line[1] for line in lines_sorted] + [line[3] for line in lines_sorted]
                        x_coords = [line[0] for line in lines_sorted] + [line[2] for line in lines_sorted]
                        
                        y_min, y_max = min(y_coords), max(y_coords)
                        x_min, x_max = min(x_coords), max(x_coords)
                        
                        zebra_lines.append((x_min, y_min, x_max - x_min, y_max - y_min))
                        
                        if self.debug:
                            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
                            cv2.putText(img, 'Pattern', (x_min, y_min-10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return zebra_lines, img
    
    def detect_zebra_crossing(self, img):
        """
        综合多种方法的斑马线检测
        """
        results = []
        processed_img = img.copy()
        
        # 方法1: 基于白色区域检测
        zebra_white, img_white = self.detect_by_white_regions(img.copy())
        results.extend(zebra_white)
        
        # 方法2: 基于形状特征检测
        white_mask = self.preprocess_image(img)
        zebra_shape, img_shape = self.detect_by_shape_features(white_mask, img.copy())
        results.extend(zebra_shape)
        
        # 方法3: 基于图案特征检测
        zebra_pattern, img_pattern = self.detect_by_pattern(img.copy(), white_mask)
        results.extend(zebra_pattern)
        
        # 合并结果（非极大值抑制）
        final_zebra_lines = self.non_max_suppression(results)
        
        return final_zebra_lines, processed_img
    
    def non_max_suppression(self, boxes, overlap_thresh=0.5):
        """
        非极大值抑制 - 合并重叠的检测框[6](@ref)
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
        
        # 绘制检测到的斑马线（使用白色框）
        for x, y, w, h in zebra_lines:
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
            cv2.putText(display_frame, 'Zebra Crossing', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
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