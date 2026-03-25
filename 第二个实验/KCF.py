import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import time
import os
import traceback

# 安全获取OpenCV版本信息
def get_opencv_version():
    """
    安全地获取OpenCV版本信息
    """
    try:
        if hasattr(cv2, '__version__'):
            version_str = cv2.__version__
            print(f"✅ OpenCV Version: {version_str}")
            return version_str
        else:
            print("⚠️ Cannot directly get OpenCV version")
            return "unknown"
    except Exception as e:
        print(f"⚠️ Error getting OpenCV version: {e}")
        return "unknown"

# 创建KCF跟踪器
def create_kcf_tracker():
    """
    创建KCF跟踪器，使用多种方法尝试
    """
    print("🔧 Trying to create KCF tracker...")
    
    # 尝试多种创建方法
    creation_methods = [
        # 方法1: 尝试legacy模块 (OpenCV 4.x)
        lambda: cv2.legacy.TrackerKCF_create() if hasattr(cv2, 'legacy') and hasattr(cv2.legacy, 'TrackerKCF_create') else None,
        
        # 方法2: 尝试直接创建 (OpenCV 3.x/4.x)
        lambda: cv2.TrackerKCF_create() if hasattr(cv2, 'TrackerKCF_create') else None,
        
        # 方法3: 尝试新API
        lambda: cv2.TrackerKCF.create() if hasattr(cv2, 'TrackerKCF') else None,
    ]
    
    for i, method in enumerate(creation_methods):
        try:
            tracker = method()
            if tracker is not None:
                print(f"✅ Method {i+1} successfully created KCF tracker")
                return tracker
        except Exception as e:
            print(f"❌ Creation method {i+1} failed: {e}")
            continue
    
    raise ValueError("❌ Cannot create KCF tracker with any method")

class KCFTracker:
    def __init__(self):
        self.trackers = []
        self.last_bboxes = []
        
    def initialize_trackers(self, frame, bboxes):
        """初始化KCF跟踪器"""
        self.trackers = []
        self.last_bboxes = []
        
        # 确保frame是3通道
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif frame.shape[2] == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        
        success_count = 0
        for i, bbox in enumerate(bboxes):
            try:
                # 创建KCF跟踪器
                tracker = create_kcf_tracker()
                
                # 验证和调整边界框
                bbox_int = self._validate_and_adjust_bbox(bbox, frame.shape)
                if bbox_int is None:
                    print(f"⚠️ Invalid bbox: {bbox}")
                    continue
                
                # 尝试初始化
                success = tracker.init(frame, bbox_int)
                if not success:
                    print(f"⚠️ KCF_{i+1} initialization failed")
                    continue
                
                self.trackers.append(tracker)
                self.last_bboxes.append(bbox_int)
                success_count += 1
                print(f"✅ KCF_{i+1} initialized successfully with bbox: {bbox_int}")
                
            except Exception as e:
                print(f"❌ KCF_{i+1} initialization error: {e}")
                continue
        
        print(f"📊 KCF tracker initialization result: {success_count}/{len(bboxes)} successful")
        return success_count > 0
    
    def _validate_and_adjust_bbox(self, bbox, frame_shape):
        """验证和调整边界框"""
        try:
            h, w = frame_shape[:2]
            x, y, bw, bh = [int(v) for v in bbox]
            
            # 检查尺寸
            if bw <= 10 or bh <= 10:
                print(f"⚠️ Bbox too small: {bw}x{bh} (min 10x10)")
                return None
            
            # 调整到图像范围内
            x = max(0, min(x, w-1))
            y = max(0, min(y, h-1))
            bw = min(bw, w - x)
            bh = min(bh, h - y)
            
            # 再次检查调整后的尺寸
            if bw <= 5 or bh <= 5:
                print(f"⚠️ Adjusted bbox still too small: {bw}x{bh}")
                return None
                
            return (x, y, bw, bh)
        except Exception as e:
            print(f"❌ Bbox adjustment error: {e}")
            return None
    
    def update(self, frame):
        """更新跟踪器"""
        bboxes = []
        success_flags = []
        
        # 确保frame是3通道
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        
        for i, tracker in enumerate(self.trackers):
            try:
                success, bbox = tracker.update(frame)
                if success and bbox is not None and bbox[2] > 5 and bbox[3] > 5:
                    self.last_bboxes[i] = bbox
                else:
                    success = False
                    bbox = self.last_bboxes[i] if i < len(self.last_bboxes) else None
            except Exception as e:
                print(f"❌ KCF_{i+1} update error: {e}")
                success = False
                bbox = self.last_bboxes[i] if i < len(self.last_bboxes) else None
            
            bboxes.append(bbox)
            success_flags.append(success)
            
        return success_flags, bboxes

class TrackingEvaluator:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    def calculate_iou(self, box1, box2):
        """计算交并比(IOU)"""
        if box1 is None or box2 is None:
            return 0
            
        try:
            x1, y1, w1, h1 = [float(v) for v in box1]
            x2, y2, w2, h2 = [float(v) for v in box2]
            
            # 计算交集区域
            xi1 = max(x1, x2)
            yi1 = max(y1, y2)
            xi2 = min(x1 + w1, x2 + w2)
            yi2 = min(y1 + h1, y2 + h2)
            
            inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
            box1_area = w1 * h1
            box2_area = w2 * h2
            union_area = box1_area + box2_area - inter_area
            
            return inter_area / union_area if union_area > 0 else 0
        except:
            return 0
    
    def calculate_center_distance(self, box1, box2):
        """计算两个边界框中心点的距离"""
        if box1 is None or box2 is None:
            return float('inf')
            
        try:
            x1, y1, w1, h1 = [float(v) for v in box1]
            x2, y2, w2, h2 = [float(v) for v in box2]
            
            center1 = (x1 + w1/2, y1 + h1/2)
            center2 = (x2 + w2/2, y2 + h2/2)
            
            return np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        except:
            return float('inf')
    
    def update_metrics(self, gt_boxes, pred_boxes, frame_idx, processing_time):
        """更新评估指标"""
        try:
            avg_iou = 0
            success_rate = 0
            avg_center_error = 0
            valid_pairs = 0
            
            for gt_box, pred_box in zip(gt_boxes, pred_boxes):
                if pred_box is not None and gt_box is not None:
                    iou = self.calculate_iou(gt_box, pred_box)
                    center_error = self.calculate_center_distance(gt_box, pred_box)
                    
                    avg_iou += iou
                    avg_center_error += center_error
                    valid_pairs += 1
                    
                    if iou > 0.3:  # IOU阈值
                        success_rate += 1
            
            if valid_pairs > 0:
                avg_iou /= valid_pairs
                success_rate /= valid_pairs
                avg_center_error /= valid_pairs
            
            self.metrics['frame_idx'].append(frame_idx)
            self.metrics['avg_iou'].append(avg_iou)
            self.metrics['success_rate'].append(success_rate)
            self.metrics['avg_center_error'].append(avg_center_error)
            self.metrics['processing_time'].append(processing_time)
            
        except Exception as e:
            print(f"❌ Error updating metrics: {e}")
    
    def get_final_metrics(self):
        """获取最终指标"""
        final_metrics = {}
        
        if len(self.metrics['avg_iou']) > 0:
            final_metrics['mean_iou'] = np.mean(self.metrics['avg_iou'])
            final_metrics['mean_success_rate'] = np.mean(self.metrics['success_rate'])
            final_metrics['mean_center_error'] = np.mean(self.metrics['avg_center_error'])
            final_metrics['total_frames'] = len(self.metrics['frame_idx'])
            
            # 计算FPS
            if np.mean(self.metrics['processing_time']) > 0:
                final_metrics['avg_fps'] = 1 / np.mean(self.metrics['processing_time'])
            else:
                final_metrics['avg_fps'] = 0
        else:
            # 如果没有数据，设置默认值
            final_metrics.update({
                'mean_iou': 0,
                'mean_success_rate': 0,
                'mean_center_error': 0,
                'total_frames': 0,
                'avg_fps': 0
            })
        
        return final_metrics

def check_opencv_installation():
    """检查OpenCV安装情况"""
    print("🔍 Checking OpenCV installation...")
    
    try:
        # 创建测试图像
        test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # 测试基本操作
        gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(test_img, (5, 5), 0)
        
        print("✅ OpenCV basic functions are normal")
        return True
    except Exception as e:
        print(f"❌ OpenCV basic function test failed: {e}")
        return False

def check_video_file(video_path):
    """检查视频文件是否存在并可读"""
    if not os.path.exists(video_path):
        print(f"❌ Video file does not exist: {video_path}")
        return False
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Cannot open video file: {video_path}")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print(f"❌ Can open video but cannot read frame: {video_path}")
        cap.release()
        return False
    
    print(f"📹 Video info: Width={frame.shape[1]}, Height={frame.shape[0]}, Channels={frame.shape[2]}")
    cap.release()
    return True

def put_text(img, text, position, font_scale=0.6, color=(255, 255, 255), thickness=2):
    """在图像上添加文本（使用英文避免中文问题）"""
    try:
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
    except Exception as e:
        print(f"Text display error: {e}")

def main():
    print("🚀 Single Object Tracking with KCF Algorithm")
    print("=" * 50)
    
    # 检查OpenCV安装
    if not check_opencv_installation():
        print("❌ OpenCV installation problem, please check installation")
        print("💡 Suggested command: pip install opencv-contrib-python")
        return
    
    # 安全获取版本信息
    opencv_version = get_opencv_version()
    
    # 设置视频路径
    video_path = r"F:\data\dete01.flv"  # 替换为您的视频路径
    
    # 检查视频文件
    if not check_video_file(video_path):
        print(f"❌ Cannot open video file: {video_path}")
        return
    
    # 初始化视频捕获
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Cannot open video file: {video_path}")
        return
    
    # 设置合适的帧延迟
    frame_delay = 30  # 视频文件可以设置较大延迟
    
    # 读取第一帧
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot read first video frame")
        cap.release()
        return
    
    print(f"📹 Video source: {video_path}, Size: {frame.shape[1]}x{frame.shape[0]}")
    
    # 选择跟踪目标
    bboxes = []
    colors = []
    
    print("\n🎯 Target Selection Instructions:")
    print("1. Drag mouse to select target area")
    print("2. Press SPACE or ENTER to confirm selection") 
    print("3. Press 'c' to cancel last selection")
    print("4. Press 'q' to end selection")
    print("=" * 50)
    
    while True:
        select_frame = frame.copy()
        put_text(select_frame, "Select ROI -> SPACE/ENTER:Confirm, c:Cancel, q:Quit", 
                (10, 30), 0.6, (0, 255, 0), 2)
        put_text(select_frame, f"Selected: {len(bboxes)} targets", 
                (10, 60), 0.6, (0, 255, 0), 2)
        
        bbox = cv2.selectROI("Select Tracking Target", select_frame, False)
        
        if bbox[2] > 10 and bbox[3] > 10:  # 最小尺寸检查
            bboxes.append(bbox)
            colors.append((np.random.randint(50, 255), 
                         np.random.randint(50, 255), 
                         np.random.randint(50, 255)))
            print(f"✅ Selected target {len(bboxes)}: {bbox}")
        else:
            print("❌ Selection area too small or invalid")
            if bbox[2] > 0 and bbox[3] > 0:
                print(f"   Selected area: {bbox} - too small (min 10x10 pixels)")
        
        # 显示已选择的目标
        display_frame = frame.copy()
        for i, (box, color) in enumerate(zip(bboxes, colors)):
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 2)
            put_text(display_frame, f"Target {i+1}", (x, y-10), 0.5, color, 1)
        
        cv2.imshow("Selected Targets", display_frame)
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('q'):
            cv2.destroyWindow("Selected Targets")
            break
        elif key == ord('c'):
            if bboxes:
                removed = bboxes.pop()
                colors.pop()
                print(f"🗑️ Removed previous selection: {removed}")
        
        cv2.destroyWindow("Selected Targets")
    
    cv2.destroyAllWindows()
    
    if not bboxes:
        print("❌ No targets selected, program exit")
        cap.release()
        return
    
    print(f"🎯 Starting to track {len(bboxes)} targets with KCF...")
    
    # 初始化KCF跟踪器
    tracker = KCFTracker()
    evaluator = TrackingEvaluator()
    
    print("🔧 Initializing KCF tracker...")
    if not tracker.initialize_trackers(frame, bboxes):
        print("❌ KCF tracker initialization failed!")
        cap.release()
        return
    
    print("✅ KCF tracker ready for tracking")
    
    # 处理视频帧
    frame_count = 0
    processing_times = []
    
    print("🎥 Starting tracking, press 'q' to quit...")
    print("💡 Tips:")
    print("   - Blue: Tracking successful")
    print("   - Gray: Tracking lost")
    print("   - Tracking works best with clear, distinctive objects")
    
    # 用于统计跟踪状态
    tracking_success = 0
    tracking_total = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("✅ Video reading completed")
            break
        
        frame_count += 1
        display_frame = frame.copy()
        
        # 更新跟踪器
        start_time = time.time()
        success_flags, pred_boxes = tracker.update(frame)
        processing_time = time.time() - start_time
        
        # 避免处理时间为0
        if processing_time == 0:
            processing_time = 0.001
            
        processing_times.append(processing_time)
        
        # 为简化实验，使用第一帧的边界框作为后续帧的ground truth
        gt_boxes = bboxes
        
        # 更新评估指标
        evaluator.update_metrics(gt_boxes, pred_boxes, frame_count, processing_time)
        
        # 更新跟踪状态统计
        for success in success_flags:
            tracking_total += 1
            if success:
                tracking_success += 1
        
        # 可视化跟踪结果
        for i, (success, bbox) in enumerate(zip(success_flags, pred_boxes)):
            if bbox is not None and bbox[2] > 0 and bbox[3] > 0:
                x, y, w, h = [int(v) for v in bbox]
                
                # 根据跟踪状态选择颜色
                if success:
                    color = (255, 0, 0)  # 蓝色表示成功
                    status_text = "OK"
                else:
                    color = (128, 128, 128)  # 灰色表示丢失
                    status_text = "LOST"
                
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), color, 2)
                put_text(display_frame, f"KCF_{i+1}({status_text})", (x, y-10), 0.5, color, 1)
                
                # 显示IOU值
                iou = evaluator.calculate_iou(gt_boxes[i], bbox) if i < len(gt_boxes) else 0
                put_text(display_frame, f"IOU: {iou:.2f}", (x, y+h+20), 0.5, color, 1)
        
        # 添加状态信息
        put_text(display_frame, f"Frame: {frame_count}", (10, 30), 0.6, (255, 255, 255), 2)
        
        # 显示实时跟踪状态
        success_rate = (tracking_success / tracking_total * 100) if tracking_total > 0 else 0
        put_text(display_frame, f"Success Rate: {success_rate:.1f}%", (10, 60), 0.6, (255, 255, 255), 2)
        
        # 显示处理速度
        if processing_times:
            current_fps = 1 / processing_times[-1] if processing_times[-1] > 0 else 0
            put_text(display_frame, f"FPS: {current_fps:.1f}", (10, 90), 0.6, (255, 255, 255), 2)
        
        put_text(display_frame, "Press 'q' to quit", (10, 120), 0.6, (255, 255, 255), 2)
        
        cv2.imshow('KCF Object Tracking', display_frame)
        
        # 每100帧显示一次进度
        if frame_count % 100 == 0:
            print(f"📊 Processed {frame_count} frames...")
        
        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            print("⏹️ Tracking stopped by user")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # 输出结果
    print("\n" + "="*50)
    print("📊 KCF Tracking Results")
    print("="*50)
    
    final_metrics = evaluator.get_final_metrics()
    
    print(f"📈 Average IOU: {final_metrics['mean_iou']:.4f}")
    print(f"✅ Success Rate: {final_metrics['mean_success_rate']:.4f} ({(tracking_success/tracking_total*100) if tracking_total > 0 else 0:.1f}% real-time)")
    print(f"🎯 Average Center Error: {final_metrics['mean_center_error']:.2f} pixels")
    print(f"⚡ Processing Speed: {final_metrics['avg_fps']:.2f} FPS")
    print(f"🎞️ Total Frames Processed: {final_metrics['total_frames']}")
    
    # 绘制性能图表
    plot_performance_results(evaluator, processing_times)

def plot_performance_results(evaluator, processing_times):
    """绘制性能图表"""
    try:
        plt.figure(figsize=(12, 8))
        
        # IOU变化曲线
        plt.subplot(2, 2, 1)
        ious = evaluator.metrics['avg_iou']
        frames = range(1, len(ious) + 1)
        plt.plot(frames, ious, 'b-', alpha=0.7, linewidth=1)
        plt.axhline(y=np.mean(ious), color='r', linestyle='--', label=f'Avg IOU: {np.mean(ious):.3f}')
        plt.xlabel('Frame Number')
        plt.ylabel('IOU')
        plt.title('KCF Tracker - IOU Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 成功率变化
        plt.subplot(2, 2, 2)
        success_rates = [rate * 100 for rate in evaluator.metrics['success_rate']]
        plt.plot(frames, success_rates, 'g-', alpha=0.7, linewidth=1)
        plt.axhline(y=np.mean(success_rates), color='r', linestyle='--', 
                   label=f'Avg Success: {np.mean(success_rates):.1f}%')
        plt.xlabel('Frame Number')
        plt.ylabel('Success Rate (%)')
        plt.title('KCF Tracker - Success Rate Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 处理速度
        plt.subplot(2, 2, 3)
        fps_values = [1/t if t > 0 else 0 for t in processing_times]
        plt.plot(frames, fps_values, 'purple', alpha=0.7, linewidth=1)
        plt.axhline(y=np.mean(fps_values), color='r', linestyle='--', 
                   label=f'Avg FPS: {np.mean(fps_values):.1f}')
        plt.xlabel('Frame Number')
        plt.ylabel('FPS')
        plt.title('KCF Tracker - Processing Speed')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 中心误差
        plt.subplot(2, 2, 4)
        center_errors = evaluator.metrics['avg_center_error']
        plt.plot(frames, center_errors, 'orange', alpha=0.7, linewidth=1)
        plt.axhline(y=np.mean(center_errors), color='r', linestyle='--', 
                   label=f'Avg Error: {np.mean(center_errors):.1f} px')
        plt.xlabel('Frame Number')
        plt.ylabel('Center Error (pixels)')
        plt.title('KCF Tracker - Center Error')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('kcf_tracking_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("\n✅ Performance chart saved as 'kcf_tracking_performance.png'")
        
    except Exception as e:
        print(f"❌ Error plotting chart: {e}")

if __name__ == "__main__":
    main()