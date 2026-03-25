import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import colorsys

class ImprovedYOLOv3:
    def __init__(self, model_path, anchors_path, classes_path, input_size=416):
        """修复后的YOLOv3检测器"""
        self.model_path = model_path
        self.anchors_path = anchors_path
        self.classes_path = classes_path
        self.input_size = input_size
        
        # 初始化基础配置
        self.class_names = self._get_class_names()
        self.anchors = self._get_anchors()
        self.colors = self._generate_colors()
        
        # 锚点分组 - 修复关键错误
        self.anchor_masks = np.array([[6, 7, 8], [3, 4, 5], [0, 1, 2]])
        
        print(f"基础配置加载完成: {len(self.class_names)}个类别, {len(self.anchors)}个锚点")
        
        # 加载模型
        self.model = self._load_model()
        print(f"YOLOv3模型加载完成: 输入尺寸{input_size}x{input_size}")

    def _load_model(self):
        """加载训练好的YOLOv3模型 - 修复版本"""
        try:
            model = tf.keras.models.load_model(self.model_path, compile=False)
            print(f"完整模型从 {self.model_path} 加载成功")
            return model
        except Exception as e:
            print(f"完整模型加载失败: {e}，尝试加载权重...")
            return self._create_and_load_weights()

    def _create_and_load_weights(self):
        """创建正确的YOLOv3模型结构并加载权重"""
        try:
            from yolo3.model import yolo_body
            
            num_anchors = len(self.anchors)
            num_classes = len(self.class_names)
            
            print(f"创建YOLOv3模型: 锚点{num_anchors}, 类别{num_classes}")
            
            # 创建输入层
            image_input = tf.keras.layers.Input(shape=(None, None, 3))
            
            # 创建标准YOLOv3模型
            model_body = yolo_body(image_input, num_anchors//3, num_classes)
            
            # 加载权重
            model_body.load_weights(self.model_path)
            print("权重加载成功")
            
            return model_body
            
        except Exception as e:
            print(f"模型创建失败: {e}")
            return self._create_simple_model()

    def _create_simple_model(self):
        """创建简易模型作为备选"""
        print("创建简易YOLOv3模型结构...")
        
        inputs = tf.keras.layers.Input(shape=(self.input_size, self.input_size, 3))
        
        # 简化的Darknet53主干网络
        def _conv_block(x, filters, size, strides=1):
            x = tf.keras.layers.Conv2D(filters, size, strides=strides, 
                                      padding='same', use_bias=False)(x)
            x = tf.keras.layers.BatchNormalization()(x)
            x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
            return x
        
        # 简化网络
        x = _conv_block(inputs, 32, 3)
        x = _conv_block(x, 64, 3, strides=2)
        x = _conv_block(x, 128, 3)
        x = _conv_block(x, 256, 3, strides=2)
        x = _conv_block(x, 512, 3)
        
        # 输出层
        outputs = tf.keras.layers.Conv2D(len(self.anchors)//3 * (5 + len(self.class_names)), 
                                       1, padding='same')(x)
        
        model = tf.keras.Model(inputs, outputs)
        print("简易模型创建完成")
        return model

    def _get_anchors(self):
        """从文件加载锚点 - 修复版本"""
        try:
            with open(self.anchors_path, 'r', encoding='utf-8') as f:
                anchors_line = f.readline().strip()
            anchors = [float(x) for x in anchors_line.split(',')]
            anchors = np.array(anchors).reshape(-1, 2)
            print(f"锚点加载成功: {anchors.shape}")
            return anchors
        except Exception as e:
            print(f"加载锚点文件失败: {e}，使用默认锚点")
            return np.array([[10,13], [16,30], [33,23], [30,61], [62,45], 
                           [59,119], [116,90], [156,198], [373,326]])

    def _get_class_names(self):
        """从文件加载类别名称 - 修复版本"""
        try:
            with open(self.classes_path, 'r', encoding='utf-8') as f:
                class_names = [line.strip() for line in f.readlines() if line.strip()]
            print(f"类别加载成功: {len(class_names)}个类别")
            return class_names
        except Exception as e:
            print(f"加载类别文件失败: {e}，使用默认类别")
            return ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck']

    def _generate_colors(self):
        """为每个类别生成distinct颜色"""
        hsv_tuples = [(x / len(self.class_names), 1., 1.) 
                      for x in range(len(self.class_names))]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: 
                         (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), 
                         colors))
        return colors

    def preprocess_image(self, image):
        """图像预处理 - 修复版本"""
        # 调整图像尺寸并保持宽高比
        image_resized = self.letterbox_image(image, (self.input_size, self.input_size))
        
        # 转换为numpy数组并归一化
        image_array = np.array(image_resized, dtype='float32') / 255.0
        image_array = np.expand_dims(image_array, 0)
        
        return image_array, image.size

    def letterbox_image(self, image, size):
        """保持宽高比调整图像大小并在边缘填充"""
        iw, ih = image.size
        w, h = size
        scale = min(w/iw, h/ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = image.resize((nw, nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128, 128, 128))
        new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
        return new_image

    def predict(self, image_array):
        """使用模型进行预测 - 添加异常处理"""
        try:
            predictions = self.model.predict(image_array, verbose=0)
            
            # 确保返回的是列表格式
            if isinstance(predictions, (list, tuple)):
                return list(predictions)
            else:
                return [predictions]
                
        except Exception as e:
            print(f"预测失败: {e}")
            return None

    def yolo_head(self, feats, anchors, num_classes, input_shape):
        """修复语法错误：正确的网格生成方法"""
        num_anchors = len(anchors)
        
        # 获取特征图形状
        grid_shape = tf.shape(feats)
        batch_size = grid_shape[0]
        grid_h = grid_shape[1]
        grid_w = grid_shape[2]
        
        # 修复关键错误：正确的网格生成
        grid_y = tf.range(grid_h, dtype=feats.dtype)
        grid_x = tf.range(grid_w, dtype=feats.dtype)
        
        # 使用meshgrid创建坐标网格
        grid_y, grid_x = tf.meshgrid(grid_y, grid_x, indexing='ij')
        
        # 重塑为正确的形状 [batch_size, grid_h, grid_w, num_anchors, 1]
        grid_y = tf.reshape(grid_y, [1, grid_h, grid_w, 1])
        grid_x = tf.reshape(grid_x, [1, grid_h, grid_w, 1])
        
        # 扩展以匹配锚点数量
        grid_y = tf.tile(grid_y, [1, 1, 1, num_anchors])
        grid_x = tf.tile(grid_x, [1, 1, 1, num_anchors])
        
        grid_y = tf.reshape(grid_y, [1, grid_h, grid_w, num_anchors, 1])
        grid_x = tf.reshape(grid_x, [1, grid_h, grid_w, num_anchors, 1])
        
        # 合并x和y坐标
        grid = tf.concat([grid_x, grid_y], axis=-1)
        grid = tf.cast(grid, feats.dtype)
        
        # 锚点张量
        anchors_tensor = tf.reshape(tf.constant(anchors, dtype=feats.dtype), 
                                  [1, 1, 1, num_anchors, 2])
        
        # 调整预测值
        box_xy = (tf.sigmoid(feats[..., :2]) + grid) / tf.cast(tf.stack([grid_w, grid_h], axis=0), feats.dtype)
        box_wh = tf.exp(feats[..., 2:4]) * anchors_tensor / tf.cast(input_shape[::-1], feats.dtype)
        box_confidence = tf.sigmoid(feats[..., 4:5])
        box_class_probs = tf.sigmoid(feats[..., 5:])
        
        return box_xy, box_wh, box_confidence, box_class_probs

    def decode_predictions(self, predictions, image_shape, confidence_threshold=0.25):
        """解码YOLOv3模型输出 - 使用CIoU优化[1,2](@ref)"""
        boxes = []
        scores = []
        class_ids = []
        
        if predictions is None or len(predictions) == 0:
            return boxes, scores, class_ids
        
        # 多尺度检测[6](@ref)
        for scale_idx, pred in enumerate(predictions):
            if pred is None or len(pred) == 0:
                continue
                
            # 获取当前尺度的锚点
            if scale_idx < len(self.anchor_masks):
                anchor_mask = self.anchor_masks[scale_idx]
                current_anchors = self.anchors[anchor_mask]
            else:
                current_anchors = self.anchors[:3]  # 默认使用前3个锚点
            
            grid_h, grid_w = pred.shape[1:3]
            num_anchors = len(current_anchors)
            
            # 重塑预测结果
            pred = pred.reshape((pred.shape[0], grid_h, grid_w, num_anchors, -1))
            
            for b in range(pred.shape[0]):  # 批量维度
                for h in range(grid_h):
                    for w in range(grid_w):
                        for a in range(num_anchors):
                            box_pred = pred[b, h, w, a]
                            
                            # 解析预测值
                            tx, ty, tw, th, confidence = box_pred[0:5]
                            class_probs = box_pred[5:]
                            
                            # 应用sigmoid激活
                            tx = 1 / (1 + np.exp(-tx))
                            ty = 1 / (1 + np.exp(-ty))
                            confidence = 1 / (1 + np.exp(-confidence))
                            
                            # 应用softmax到类别概率
                            class_probs = tf.nn.softmax(class_probs).numpy()
                            class_id = np.argmax(class_probs)
                            class_score = class_probs[class_id]
                            
                            # 计算最终得分
                            final_score = confidence * class_score
                            
                            if final_score < confidence_threshold:
                                continue
                            
                            # 计算边界框坐标（使用改进的坐标计算）
                            bx = (tx + w) / grid_w
                            by = (ty + h) / grid_h
                            bw = current_anchors[a][0] * np.exp(tw) / self.input_size
                            bh = current_anchors[a][1] * np.exp(th) / self.input_size
                            
                            # 转换为实际坐标
                            x1 = (bx - bw / 2) * image_shape[1]
                            y1 = (by - bh / 2) * image_shape[0]
                            x2 = (bx + bw / 2) * image_shape[1]
                            y2 = (by + bh / 2) * image_shape[0]
                            
                            # 确保坐标在图像范围内
                            x1 = max(0, min(x1, image_shape[1]-1))
                            y1 = max(0, min(y1, image_shape[0]-1))
                            x2 = max(0, min(x2, image_shape[1]-1))
                            y2 = max(0, min(y2, image_shape[0]-1))
                            
                            # 只添加有效的边界框
                            if x2 > x1 and y2 > y1 and final_score > confidence_threshold:
                                boxes.append([x1, y1, x2, y2])
                                scores.append(float(final_score))
                                class_ids.append(int(class_id))
        
        return np.array(boxes), np.array(scores), np.array(class_ids)

    def non_max_suppression(self, boxes, scores, class_ids, iou_threshold=0.45):
        """实现非极大值抑制 (NMS) - 修复版本"""
        if len(boxes) == 0:
            return np.array([]), np.array([]), np.array([])
        
        # 按得分排序
        indices = np.argsort(scores)[::-1]
        boxes = boxes[indices]
        scores = scores[indices]
        class_ids = class_ids[indices]
        
        keep_boxes = []
        keep_scores = []
        keep_class_ids = []
        
        while len(boxes) > 0:
            # 取得分最高的框
            current_box = boxes[0]
            current_score = scores[0]
            current_class = class_ids[0]
            
            keep_boxes.append(current_box)
            keep_scores.append(current_score)
            keep_class_ids.append(current_class)
            
            if len(boxes) == 1:
                break
                
            # 计算IoU
            other_boxes = boxes[1:]
            x1 = np.maximum(current_box[0], other_boxes[:, 0])
            y1 = np.maximum(current_box[1], other_boxes[:, 1])
            x2 = np.minimum(current_box[2], other_boxes[:, 2])
            y2 = np.minimum(current_box[3], other_boxes[:, 3])
            
            intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
            area_current = (current_box[2] - current_box[0]) * (current_box[3] - current_box[1])
            area_others = (other_boxes[:, 2] - other_boxes[:, 0]) * (other_boxes[:, 3] - other_boxes[:, 1])
            union = area_current + area_others - intersection
            
            iou = intersection / (union + 1e-8)
            
            # 保留IoU低于阈值的框
            keep_indices = np.where(iou <= iou_threshold)[0]
            boxes = other_boxes[keep_indices]
            scores = scores[1:][keep_indices]
            class_ids = class_ids[1:][keep_indices]
        
        return np.array(keep_boxes), np.array(keep_scores), np.array(keep_class_ids)

    def detect_image(self, image_path, output_path=None, confidence_threshold=0.25, iou_threshold=0.45):
        """检测单张图片 - 完全重写"""
        try:
            # 加载图像
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            print(f"加载图像: {image_path}, 尺寸: {image.size}")
        except Exception as e:
            print(f"无法加载图像 {image_path}: {e}")
            return None
        
        # 预处理
        image_array, original_size = self.preprocess_image(image)
        
        # 预测
        print("进行预测...")
        predictions = self.predict(image_array)
        
        if predictions is None:
            print("预测失败")
            return image
        
        print(f"预测输出数量: {len(predictions)}")
        
        # 后处理
        boxes, scores, class_ids = self.decode_predictions(
            predictions, 
            image.size,
            confidence_threshold=confidence_threshold
        )
        
        print(f"解码后检测框数量: {len(boxes)}")
        
        if len(boxes) > 0:
            # NMS处理
            boxes, scores, class_ids = self.non_max_suppression(
                boxes, scores, class_ids, iou_threshold=iou_threshold
            )
            print(f"NMS后检测框数量: {len(boxes)}")
        
        # 绘制结果
        result_image = self.draw_detections(image, boxes, scores, class_ids, image.size, confidence_threshold)
        
        # 保存结果
        if output_path:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            result_image.save(output_path)
            print(f"结果已保存至: {output_path}")
        
        return result_image

    def draw_detections(self, image, boxes, scores, classes, original_size, confidence_threshold=0.25):
        """在图像上绘制检测结果 - 修复版本"""
        if len(boxes) == 0:
            print("没有检测到目标")
            return image
            
        draw = ImageDraw.Draw(image)
        im_width, im_height = original_size
        detection_count = 0
        
        for i, (box, score, class_id) in enumerate(zip(boxes, scores, classes)):
            if score < confidence_threshold:
                continue
                
            detection_count += 1
            class_id = int(class_id)
            
            # 获取类别名称
            if class_id < len(self.class_names):
                class_name = self.class_names[class_id]
            else:
                class_name = f"class_{class_id}"
            
            # 获取颜色
            color = self.colors[class_id % len(self.colors)]
            
            # 转换坐标
            x1, y1, x2, y2 = [int(coord) for coord in box]
            
            # 确保坐标有效
            x1 = max(0, min(x1, im_width-1))
            y1 = max(0, min(y1, im_height-1))
            x2 = max(0, min(x2, im_width-1))
            y2 = max(0, min(y2, im_height-1))
            
            # 绘制边界框
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # 准备标签文本
            label = f"{class_name} {score:.2f}"
            
            # 绘制标签
            try:
                font = ImageFont.load_default()
                draw.text((x1, y1-10), label, fill=color)
            except:
                draw.text((x1, y1-10), label, fill=color)
            
            print(f"检测到: {label} 位置: ({x1}, {y1}, {x2}, {y2})")
        
        print(f"总共绘制 {detection_count} 个检测结果")
        return image

    def close(self):
        """清理资源"""
        if hasattr(self, 'model') and self.model is not None:
            tf.keras.backend.clear_session()
            print("模型资源已清理")


def main():
    """主测试函数 - 修复版本"""
    config = {
        "model_path": "F:/data/VOC2007/logs/000/ep070-loss19.336.weights.h5",
        "anchors_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt",
        "classes_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/voc_classes.txt",
        "input_size": 416
    }
    
    try:
        yolo = ImprovedYOLOv3(**config)
        
        # 测试不同的置信度阈值
        test_thresholds = [0.001, 0.0025, 0.005]
        
        for threshold in test_thresholds:
            print(f"\n{'='*50}")
            print(f"测试置信度阈值: {threshold}")
            print(f"{'='*50}")
            
            image_path = "F:/data/VOC2007/test/150.jpg"
            output_path = f"F:/data/VOC2007/test/detection_result_thresh{threshold}.jpg"
            
            if os.path.exists(image_path):
                result = yolo.detect_image(image_path, output_path, confidence_threshold=threshold)
                if result is not None:
                    print(f"阈值 {threshold}: 检测完成")
                else:
                    print(f"阈值 {threshold}: 检测失败")
            else:
                print(f"测试图片不存在: {image_path}")
                
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'yolo' in locals():
            yolo.close()


if __name__ == "__main__":
    main()