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
        """图像预处理"""
        # 灰度转换
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 高斯滤波去噪
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 自适应阈值处理
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        
        # 形态学操作 - 开运算
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        return processed
    
    def detect_zebra_crossing(self, processed_img, original_img):
        """检测斑马线"""
        # 查找轮廓
        contours, _ = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        zebra_lines = []
        detection_mask = np.zeros_like(processed_img)
        
        for contour in contours:
            # 过滤小面积区域
            if cv2.contourArea(contour) < 500:
                continue
                
            # 获取边界矩形
            x, y, w, h = cv2.boundingRect(contour)
            
            # 斑马线特征：长宽比大，水平方向延伸
            aspect_ratio = w / h
            if aspect_ratio > 3 and w > 100 and h < 50:
                zebra_lines.append((x, y, w, h))
                cv2.drawContours(detection_mask, [contour], -1, 255, -1)
                
                if self.debug:
                    cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        return zebra_lines, detection_mask, original_img
    
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
    
    def visualize_detection(self, frame, zebra_lines, detection_mask, result):
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
        
        # 显示检测掩码
        detection_display = cv2.applyColorMap(detection_mask, cv2.COLORMAP_JET)
        
        return display_frame, detection_display
    
    def process_video(self, video_path, ground_truth_callback=None):
        """处理视频流"""
        # 首先检查文件是否存在
        if not os.path.exists(video_path):
            print(f"错误：视频文件不存在于路径 '{video_path}'")
            # 返回一个空的报告字典而不是 None
            return self.get_performance_report()
        
        # 检查文件扩展名是否常见（可选，但有助于调试）
        valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        file_extension = os.path.splitext(video_path)[1].lower()
        if file_extension not in valid_extensions:
            print(f"警告：文件扩展名 '{file_extension}' 可能不受良好支持。尝试使用以下扩展名：{valid_extensions}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"错误：无法打开视频文件 '{video_path}'")
            print("可能的原因：")
            print("1. 文件路径不正确")
            print("2. 文件格式或编解码器不受支持")
            print("3. 缺少必要的解码器（如FFmpeg）")
            print("4. 文件可能已损坏或不完整")
            # 返回一个空的报告字典而不是 None
            return self.get_performance_report()
        
        frame_count = 0
        start_time = time.time()
        
        # 获取视频的总帧数（用于进度信息）
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"视频打开成功！总帧数约为：{total_frames}")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"已处理完所有帧或读取失败（帧 {frame_count}）")
                break
            
            frame_count += 1
            
            # 预处理图像
            processed = self.preprocess_image(frame)
            
            # 检测斑马线
            zebra_lines, detection_mask, annotated_frame = self.detect_zebra_crossing(processed, frame.copy())
            
            # 评估检测结果
            ground_truth = ground_truth_callback(frame_count) if ground_truth_callback else False
            detected = len(zebra_lines) > 0
            result = self.calculate_metrics(detected, ground_truth)
            self.detection_history.append(result)
            
            # 可视化结果
            display_frame, detection_display = self.visualize_detection(
                annotated_frame, zebra_lines, detection_mask, result
            )
            
            # 显示结果
            cv2.imshow('Original Frame', display_frame)
            cv2.imshow('Processing Steps', self.create_processing_stack(frame, processed, detection_mask))
            cv2.imshow('Detection Mask', detection_display)
            
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
    
    def create_processing_stack(self, original, processed, detection_mask):
        """创建处理步骤的可视化堆栈"""
        # 调整大小以便堆叠
        height, width = original.shape[:2]
        display_size = (width // 2, height // 2)
        
        # 调整图像大小
        orig_resized = cv2.resize(original, display_size)
        proc_resized = cv2.resize(processed, display_size)
        mask_resized = cv2.resize(detection_mask, display_size)
        
        # 转换为彩色以便显示
        proc_colored = cv2.cvtColor(proc_resized, cv2.COLOR_GRAY2BGR)
        mask_colored = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2BGR)
        
        # 添加标签
        cv2.putText(orig_resized, 'Original', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(proc_colored, 'Processed', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(mask_colored, 'Detection Mask', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 堆叠图像
        top_row = np.hstack([orig_resized, proc_colored])
        bottom_row = np.hstack([mask_colored, np.zeros_like(mask_colored)])
        processing_stack = np.vstack([top_row, bottom_row])
        
        return processing_stack

# 使用示例
if __name__ == "__main__":
    # 初始化检测器（设置debug=True可以看到更多处理细节）
    detector = ZebraCrossingDetector(debug=True)
    
    # 简单的真实标签生成函数（实际使用时需要根据具体视频实现）
    def simple_ground_truth(frame_number):
        # 这是一个示例函数，实际使用时需要根据视频内容实现
        # 例如：在第10-20帧和第50-60帧有斑马线
        if (10 <= frame_number <= 20) or (50 <= frame_number <= 60):
            return True
        return False
    
    # 处理视频 - 使用实际存在的视频路径
    # 注意：将下面的路径替换为你实际的视频文件路径
    video_path = "F:/PycharmProjects/pythonProject/大四上专项课/人工智能基础算法（学生版）/LAB13/斑马线2.mp4"
    
    # 在尝试处理前检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误：请确保视频文件存在于此路径：{video_path}")
        print("正在创建示例性能报告...")
        # 创建一个空的报告，避免后续错误
        report = detector.get_performance_report()
    else:
        # 处理视频
        report = detector.process_video(video_path, simple_ground_truth)
    
    # 保存报告到文件
    if report is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"zebra_detection_report_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("斑马线检测报告\n")
            f.write("=" * 40 + "\n")
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
        
        print(f"\n报告已保存至: {report_filename}")
    else:
        print("未能生成报告，无法保存。")