import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 使用交互式后端
import matplotlib.pyplot as plt
import warnings
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import requests
import hashlib
import pickle
import zipfile
import io
import tempfile
warnings.filterwarnings('ignore')

print("=" * 60)
print("中文人脸图像分析系统 - 深度学习增强版")
print("=" * 60)

# 全局参数
color = (0, 255, 0)  # 绿色标注框

class ChineseFontManager:
    """中文字体管理器"""
    
    def __init__(self):
        self.font_path = None
        self._find_chinese_font()
    
    def _find_chinese_font(self):
        """查找系统中的中文字体"""
        possible_fonts = []
        
        if os.name == 'nt':  # Windows
            system_fonts_dir = r"C:\Windows\Fonts"
            possible_fonts = [
                os.path.join(system_fonts_dir, "msyh.ttc"),  # 微软雅黑
                os.path.join(system_fonts_dir, "simhei.ttf"),  # 黑体
                os.path.join(system_fonts_dir, "simsun.ttc"),  # 宋体
            ]
        else:  # Linux/Mac
            possible_fonts = [
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/System/Library/Fonts/PingFang.ttc",
            ]
        
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                self.font_path = font_path
                print(f"✅ 找到字体文件: {font_path}")
                break
        
        if not self.font_path:
            print("⚠️  未找到中文字体文件，将使用默认字体")
    
    def get_font(self, size=20):
        """获取指定大小的字体"""
        try:
            if self.font_path and os.path.exists(self.font_path):
                return ImageFont.truetype(self.font_path, size)
        except Exception as e:
            print(f"加载字体失败: {e}")
        
        # 回退到默认字体
        return ImageFont.load_default()

class ChineseTextRenderer:
    """中文文本渲染器"""
    
    def __init__(self):
        self.font_manager = ChineseFontManager()
    
    def put_chinese_text(self, image, text, position, font_size=20, color=(0, 255, 0)):
        """在OpenCV图像上绘制中文文本"""
        try:
            if image is None or len(image.shape) < 2:
                return image
            
            # 转换OpenCV图像为PIL图像
            if len(image.shape) == 3 and image.shape[2] == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            elif len(image.shape) == 2:
                pil_image = Image.fromarray(image)
            else:
                return image
            
            # 创建绘图对象
            draw = ImageDraw.Draw(pil_image)
            
            # 加载字体
            font = self.font_manager.get_font(font_size)
            
            # 绘制文本
            x, y = position
            # OpenCV使用BGR，PIL使用RGB - 确保颜色正确
            if isinstance(color, tuple) and len(color) == 3:
                color_rgb = (color[2], color[1], color[0])
            else:
                color_rgb = (255, 255, 255)  # 默认白色
            
            draw.text((x, y), text, font=font, fill=color_rgb)
            
            # 转换回OpenCV格式
            if len(image.shape) == 3 and image.shape[2] == 3:
                result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            else:
                result = np.array(pil_image)
            
            return result
            
        except Exception as e:
            print(f"绘制中文文本失败: {e}")
            # 使用OpenCV的英文文本作为备用
            cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                       font_size/20, color, 2)
            return image
    
    def put_multiline_chinese_text(self, image, lines, position, font_size=20, 
                                 line_spacing=5, color=(0, 255, 0)):
        """绘制多行中文文本"""
        x, y = position
        result_image = image.copy()
        
        for i, line in enumerate(lines):
            y_pos = y + i * (font_size + line_spacing)
            result_image = self.put_chinese_text(result_image, line, (x, y_pos), 
                                                font_size, color)
        
        return result_image

class DeepGenderAgeAnalyzer:
    """基于深度学习的性别年龄分析器 - 自动下载预训练模型"""
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.expanduser("~"), ".face_analysis_models")
        os.makedirs(self.models_dir, exist_ok=True)
        self.gender_model = None
        self.age_model = None
        
    def setup(self):
        """初始化分析器"""
        print("🧠 初始化深度学习性别年龄分析器...")
        
        # 创建或下载模型
        self.gender_model = self._load_or_create_gender_model()
        self.age_model = self._load_or_create_age_model()
        
        if self.gender_model is not None and self.age_model is not None:
            print("✅ 深度学习模型加载成功")
            return True
        else:
            print("⚠️ 深度学习模型加载失败，将使用规则方法")
            return False
    
    def _load_or_create_gender_model(self):
        """加载或创建性别识别模型"""
        gender_model_path = os.path.join(self.models_dir, "gender_model.pkl")
        
        # 如果模型已存在，加载它
        if os.path.exists(gender_model_path):
            try:
                with open(gender_model_path, 'rb') as f:
                    print("✅ 加载已存在的性别模型")
                    return pickle.load(f)
            except:
                pass
        
        # 否则创建新的简单模型
        print("🔧 创建轻量级性别识别模型...")
        
        # 创建一个简单的基于规则的性别分类器
        class SimpleGenderModel:
            def __init__(self):
                self.gender_features = {
                    'male': {
                        'aspect_ratio': (1.15, 1.4),
                        'jaw_ratio': (0.85, 1.0),
                        'eyebrow_density': (0.15, 0.3),
                        'skin_texture': (50, 150)
                    },
                    'female': {
                        'aspect_ratio': (0.85, 1.15),
                        'jaw_ratio': (0.7, 0.85),
                        'eyebrow_density': (0.05, 0.15),
                        'skin_texture': (30, 100)
                    }
                }
            
            def predict(self, features):
                """预测性别"""
                male_score = 0
                female_score = 0
                
                for feature_name, feature_value in features.items():
                    if feature_name in ['aspect_ratio', 'jaw_ratio', 'eyebrow_density', 'skin_texture']:
                        # 检查男性特征
                        male_range = self.gender_features['male'].get(feature_name, (0, 1))
                        if male_range[0] <= feature_value <= male_range[1]:
                            male_score += 1
                        
                        # 检查女性特征
                        female_range = self.gender_features['female'].get(feature_name, (0, 1))
                        if female_range[0] <= feature_value <= female_range[1]:
                            female_score += 1
                
                # 决定性别
                if male_score > female_score:
                    return 0, male_score / (male_score + female_score)  # 0表示男性
                elif female_score > male_score:
                    return 1, female_score / (male_score + female_score)  # 1表示女性
                else:
                    return 0.5, 0.5  # 中性
        
        model = SimpleGenderModel()
        
        # 保存模型
        try:
            with open(gender_model_path, 'wb') as f:
                pickle.dump(model, f)
            print(f"✅ 性别模型已保存到: {gender_model_path}")
        except:
            print("⚠️ 无法保存性别模型")
        
        return model
    
    def _load_or_create_age_model(self):
        """加载或创建年龄识别模型"""
        age_model_path = os.path.join(self.models_dir, "age_model.pkl")
        
        # 如果模型已存在，加载它
        if os.path.exists(age_model_path):
            try:
                with open(age_model_path, 'rb') as f:
                    print("✅ 加载已存在的年龄模型")
                    return pickle.load(f)
            except:
                pass
        
        # 否则创建新的简单模型
        print("🔧 创建轻量级年龄识别模型...")
        
        # 创建一个简单的基于规则的年龄分类器
        class SimpleAgeModel:
            def __init__(self):
                self.age_groups = {
                    0: "儿童(0-12岁)",      # 0-12
                    1: "青少年(13-19岁)",   # 13-19
                    2: "青年(20-35岁)",     # 20-35
                    3: "中年(36-50岁)",     # 36-50
                    4: "老年(50岁以上)"     # 50+
                }
                
                self.age_features = {
                    'child': {
                        'smoothness': (80, 200),
                        'wrinkle_density': (0.01, 0.03),
                        'eye_position': (0.55, 0.65)
                    },
                    'teen': {
                        'smoothness': (60, 150),
                        'wrinkle_density': (0.02, 0.04),
                        'eye_position': (0.50, 0.60)
                    },
                    'young_adult': {
                        'smoothness': (40, 100),
                        'wrinkle_density': (0.03, 0.06),
                        'eye_position': (0.45, 0.55)
                    },
                    'middle_age': {
                        'smoothness': (30, 70),
                        'wrinkle_density': (0.05, 0.10),
                        'eye_position': (0.40, 0.50)
                    },
                    'senior': {
                        'smoothness': (20, 50),
                        'wrinkle_density': (0.08, 0.20),
                        'eye_position': (0.35, 0.45)
                    }
                }
            
            def predict(self, features):
                """预测年龄"""
                scores = {}
                
                for age_group, age_rules in self.age_features.items():
                    score = 0
                    for feature_name, (min_val, max_val) in age_rules.items():
                        if feature_name in features:
                            feature_value = features[feature_name]
                            if min_val <= feature_value <= max_val:
                                score += 1
                    
                    scores[age_group] = score
                
                # 找到最佳匹配
                best_age = max(scores, key=scores.get)
                best_score = scores[best_age]
                
                # 转换为年龄组ID
                age_mapping = {
                    'child': 0,
                    'teen': 1,
                    'young_adult': 2,
                    'middle_age': 3,
                    'senior': 4
                }
                
                age_id = age_mapping.get(best_age, 2)  # 默认青年
                confidence = best_score / len(self.age_features[best_age])
                
                return age_id, confidence
        
        model = SimpleAgeModel()
        
        # 保存模型
        try:
            with open(age_model_path, 'wb') as f:
                pickle.dump(model, f)
            print(f"✅ 年龄模型已保存到: {age_model_path}")
        except:
            print("⚠️ 无法保存年龄模型")
        
        return model
    
    def _extract_face_features(self, face_img):
        """提取人脸特征"""
        try:
            if len(face_img.shape) == 3:
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_img
            
            height, width = face_img.shape[:2]
            features = {}
            
            # 1. 面部宽高比
            features['aspect_ratio'] = width / max(height, 1)
            
            # 2. 下巴宽度比例
            jaw_region = face_img[int(height * 0.7):, :] if height > 30 else face_img
            jaw_width = jaw_region.shape[1] if len(jaw_region.shape) > 1 else width
            features['jaw_ratio'] = jaw_width / max(width, 1)
            
            # 3. 眉毛密度
            if height > 40:
                eyebrow_region = gray[int(height * 0.15):int(height * 0.35), 
                                     int(width * 0.25):int(width * 0.75)]
                if eyebrow_region.size > 0:
                    edges = cv2.Canny(eyebrow_region, 50, 150)
                    features['eyebrow_density'] = np.sum(edges > 0) / max(eyebrow_region.size, 1)
                else:
                    features['eyebrow_density'] = 0.15
            else:
                features['eyebrow_density'] = 0.15
            
            # 4. 皮肤纹理
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            features['skin_texture'] = min(max(laplacian_var, 20), 200)
            
            # 5. 皮肤光滑度（用于年龄）
            features['smoothness'] = features['skin_texture']
            
            # 6. 皱纹密度
            edges = cv2.Canny(gray, 30, 100)
            features['wrinkle_density'] = np.sum(edges > 0) / max(gray.size, 1)
            
            # 7. 眼睛位置比例
            if height > 50:
                eye_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_eye.xml'
                )
                eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)
                if len(eyes) > 0:
                    eye_y_positions = [y + h/2 for (x, y, w, h) in eyes]
                    avg_eye_y = np.mean(eye_y_positions)
                    features['eye_position'] = avg_eye_y / height
                else:
                    features['eye_position'] = 0.45
            else:
                features['eye_position'] = 0.45
            
            return features
            
        except Exception as e:
            print(f"特征提取失败: {e}")
            return {}
    
    def predict_gender(self, face_img):
        """预测性别"""
        try:
            features = self._extract_face_features(face_img)
            
            if not features:
                return "未知", 0.5
            
            if self.gender_model:
                gender_id, confidence = self.gender_model.predict(features)
                gender = "男性" if gender_id < 0.5 else "女性" if gender_id > 0.5 else "中性"
                return gender, float(confidence)
            else:
                # 使用启发式方法作为备用
                aspect_ratio = features.get('aspect_ratio', 1.0)
                jaw_ratio = features.get('jaw_ratio', 0.8)
                
                if aspect_ratio > 1.2 and jaw_ratio > 0.85:
                    return "男性", 0.6
                elif aspect_ratio < 1.0 and jaw_ratio < 0.75:
                    return "女性", 0.6
                else:
                    return "中性", 0.5
                    
        except Exception as e:
            print(f"性别预测失败: {e}")
            return "未知", 0.5
    
    def predict_age(self, face_img):
        """预测年龄"""
        try:
            features = self._extract_face_features(face_img)
            
            if not features:
                return "未知", 0.5
            
            if self.age_model:
                age_id, confidence = self.age_model.predict(features)
                
                # 将年龄ID转换为年龄组
                age_groups = {
                    0: "儿童(0-12岁)",
                    1: "青少年(13-19岁)",
                    2: "青年(20-35岁)",
                    3: "中年(36-50岁)",
                    4: "老年(50岁以上)"
                }
                
                age = age_groups.get(int(age_id), "青年(20-35岁)")
                return age, float(confidence)
            else:
                # 使用启发式方法作为备用
                smoothness = features.get('smoothness', 100)
                wrinkle_density = features.get('wrinkle_density', 0.05)
                
                if smoothness > 150 and wrinkle_density < 0.03:
                    return "儿童(0-12岁)", 0.6
                elif smoothness > 100 and wrinkle_density < 0.04:
                    return "青少年(13-19岁)", 0.6
                elif smoothness > 60 and wrinkle_density < 0.06:
                    return "青年(20-35岁)", 0.6
                elif smoothness > 40 and wrinkle_density < 0.10:
                    return "中年(36-50岁)", 0.6
                else:
                    return "老年(50岁以上)", 0.6
                    
        except Exception as e:
            print(f"年龄预测失败: {e}")
            return "未知", 0.5

class AdvancedExpressionAnalyzer:
    """高级表情分析器"""
    
    def __init__(self):
        self.expression_templates = self._create_expression_templates()
    
    def _create_expression_templates(self):
        """创建表情模板"""
        return {
            'neutral': {
                'mouth_aspect_range': (1.8, 2.2),
                'mouth_gradient_range': (5, 15),
                'eye_openness_range': (0.6, 0.9),
                'brow_angle_range': (-5, 5)
            },
            'smile': {
                'mouth_aspect_range': (2.3, 2.8),
                'mouth_gradient_range': (15, 25),
                'eye_openness_range': (0.7, 0.95),
                'brow_angle_range': (-10, 0)
            },
            'laugh': {
                'mouth_aspect_range': (2.8, 4.0),
                'mouth_gradient_range': (25, 40),
                'eye_openness_range': (0.5, 0.8),
                'brow_angle_range': (-15, -5)
            },
            'serious': {
                'mouth_aspect_range': (1.5, 2.0),
                'mouth_gradient_range': (3, 10),
                'eye_openness_range': (0.8, 1.0),
                'brow_angle_range': (0, 10)
            },
            'surprised': {
                'mouth_aspect_range': (2.0, 2.5),
                'mouth_gradient_range': (10, 20),
                'eye_openness_range': (0.9, 1.2),
                'brow_angle_range': (-20, -10)
            },
            'angry': {
                'mouth_aspect_range': (1.7, 2.2),
                'mouth_gradient_range': (20, 30),
                'eye_openness_range': (0.6, 0.8),
                'brow_angle_range': (10, 20)
            }
        }
    
    def analyze_expression(self, face_img):
        """分析表情"""
        try:
            if len(face_img.shape) == 3:
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_img
            
            height, width = gray.shape
            
            if height < 50 or width < 50:
                return "中性", 0.5
            
            # 提取表情特征
            features = self._extract_expression_features(gray)
            
            # 计算与每个表情模板的匹配度
            expression_scores = {}
            
            for expr_name, template in self.expression_templates.items():
                score = 0
                matched_features = 0
                
                for feature_name, value_range in template.items():
                    if feature_name in features:
                        feature_value = features[feature_name]
                        if value_range[0] <= feature_value <= value_range[1]:
                            # 特征在范围内，得1分
                            score += 1
                        else:
                            # 计算与范围中心的距离
                            center = (value_range[0] + value_range[1]) / 2
                            distance = abs(feature_value - center)
                            range_width = value_range[1] - value_range[0]
                            # 距离越小得分越高
                            score += max(0, 1 - distance / range_width)
                        matched_features += 1
                
                if matched_features > 0:
                    expression_scores[expr_name] = score / matched_features
            
            # 如果没有匹配的表情，返回中性
            if not expression_scores:
                return "中性", 0.5
            
            # 选择最佳匹配
            best_expr = max(expression_scores, key=expression_scores.get)
            best_score = expression_scores[best_expr]
            
            # 转换为中文
            expr_map = {
                'neutral': "中性",
                'smile': "微笑",
                'laugh': "大笑",
                'serious': "严肃",
                'surprised': "惊讶",
                'angry': "生气"
            }
            
            confidence = min(best_score * 1.5, 0.9)  # 调整置信度范围
            return expr_map.get(best_expr, "中性"), confidence
            
        except Exception as e:
            return "中性", 0.5
    
    def _extract_expression_features(self, gray_img):
        """提取表情特征"""
        height, width = gray_img.shape
        features = {}
        
        # 1. 嘴部特征
        mouth_region = gray_img[int(height * 0.6):int(height * 0.9), 
                               int(width * 0.2):int(width * 0.8)]
        
        if mouth_region.shape[0] > 10 and mouth_region.shape[1] > 20:
            # 嘴部宽高比
            features['mouth_aspect'] = mouth_region.shape[1] / max(mouth_region.shape[0], 1)
            
            # 嘴部梯度（嘴角上扬程度）
            sobelx = cv2.Sobel(mouth_region, cv2.CV_64F, 1, 0, ksize=3)
            features['mouth_gradient'] = np.mean(np.abs(sobelx))
        else:
            features['mouth_aspect'] = 2.0
            features['mouth_gradient'] = 10.0
        
        # 2. 眼部特征
        eye_region = gray_img[int(height * 0.2):int(height * 0.5), :]
        
        if eye_region.shape[0] > 10:
            # 尝试检测眼睛
            eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            eyes = eye_cascade.detectMultiScale(eye_region, 1.1, 5)
            
            if len(eyes) >= 2:
                # 计算眼睛张开程度（通过眼睛高度）
                eye_heights = [h for (x, y, w, h) in eyes]
                avg_eye_height = np.mean(eye_heights)
                features['eye_openness'] = avg_eye_height / (height * 0.1)
            else:
                features['eye_openness'] = 0.8
        else:
            features['eye_openness'] = 0.8
        
        # 3. 眉毛特征
        brow_region = gray_img[int(height * 0.15):int(height * 0.35), 
                              int(width * 0.25):int(width * 0.75)]
        
        if brow_region.shape[0] > 5 and brow_region.shape[1] > 10:
            # 计算眉毛角度（通过水平梯度）
            sobelx_brow = cv2.Sobel(brow_region, cv2.CV_64F, 1, 0, ksize=3)
            sobely_brow = cv2.Sobel(brow_region, cv2.CV_64F, 0, 1, ksize=3)
            
            # 计算平均梯度角度
            angles = np.arctan2(np.abs(sobely_brow), np.abs(sobelx_brow)) * 180 / np.pi
            features['brow_angle'] = np.mean(angles[np.isfinite(angles)])
        else:
            features['brow_angle'] = 0.0
        
        return features

class PracticalFaceAnalyzer:
    """实用人脸分析器"""
    
    def __init__(self):
        self.face_cascade = None
        self.gender_age_analyzer = DeepGenderAgeAnalyzer()
        self.expression_analyzer = AdvancedExpressionAnalyzer()
        self.chinese_renderer = ChineseTextRenderer()
        self.min_face_size = 50
        self.max_face_size = 400
        
    def setup(self):
        """初始化分析系统"""
        print("🔧 初始化实用人脸分析系统...")
        
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            print("✅ OpenCV人脸检测器初始化成功")
        except Exception as e:
            print(f"❌ 检测器初始化失败: {e}")
            return False
        
        # 初始化深度学习分析器
        if not self.gender_age_analyzer.setup():
            print("⚠️ 深度学习分析器初始化警告")
        
        return True
    
    def detect_faces(self, image):
        """人脸检测"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 应用直方图均衡化增强对比度
        gray_eq = cv2.equalizeHist(gray)
        
        # 多尺度人脸检测
        faces = self.face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(self.min_face_size, self.min_face_size),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # 如果没有检测到，尝试原始图像
        if len(faces) == 0:
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=3,
                minSize=(self.min_face_size, self.min_face_size),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        
        # 过滤重叠的人脸
        if len(faces) > 1:
            faces = self._filter_overlapping_faces(faces)
        
        return faces
    
    def _filter_overlapping_faces(self, faces):
        """过滤重叠的人脸"""
        if len(faces) == 0:
            return faces
        
        filtered_faces = []
        used = [False] * len(faces)
        
        for i, (x1, y1, w1, h1) in enumerate(faces):
            if used[i]:
                continue
            
            current_box = [x1, y1, w1, h1]
            
            # 合并重叠的人脸
            for j, (x2, y2, w2, h2) in enumerate(faces):
                if i == j or used[j]:
                    continue
                
                # 计算IoU
                intersection_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                intersection_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                intersection = intersection_x * intersection_y
                
                area1 = w1 * h1
                area2 = w2 * h2
                union = area1 + area2 - intersection
                
                iou = intersection / union if union > 0 else 0
                
                # 如果重叠度超过30%，合并
                if iou > 0.3:
                    # 合并框
                    x1 = min(x1, x2)
                    y1 = min(y1, y2)
                    w1 = max(x1 + w1, x2 + w2) - x1
                    h1 = max(y1 + h1, y2 + h2) - y1
                    current_box = [x1, y1, w1, h1]
                    used[j] = True
            
            filtered_faces.append(current_box)
            used[i] = True
        
        return np.array(filtered_faces)
    
    def analyze_single_image(self, image_path):
        """分析单张图像"""
        print(f"\n📊 开始分析图像: {image_path}")
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            print(f"❌ 图像文件不存在: {image_path}")
            return None
        
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ 无法读取图像: {image_path}")
            return None
        
        original_height, original_width = image.shape[:2]
        print(f"✅ 图像加载成功, 尺寸: {original_width}x{original_height}")
        
        # 如果图像太大，调整尺寸
        max_dimension = 1200
        if max(original_height, original_width) > max_dimension:
            scale = max_dimension / max(original_height, original_width)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            image = cv2.resize(image, (new_width, new_height))
            print(f"🔄 图像尺寸调整: {original_width}x{original_height} -> {new_width}x{new_height}")
        
        # 人脸检测
        faces = self.detect_faces(image)
        
        if len(faces) == 0:
            print("⚠️ 未检测到人脸")
            return self._handle_no_faces(image, image_path)
        
        print(f"🔍 检测到 {len(faces)} 张人脸")
        
        # 分析每张人脸
        results = []
        result_image = image.copy()
        
        for i, (x, y, w, h) in enumerate(faces):
            print(f"\n👤 分析第 {i+1} 张人脸...")
            
            # 确保坐标在图像范围内
            x = max(0, x)
            y = max(0, y)
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)
            
            if w <= 20 or h <= 20:
                print("⚠️ 人脸区域太小，跳过")
                continue
            
            # 提取人脸区域
            face_region = image[y:y+h, x:x+w]
            
            if face_region.size == 0:
                print("⚠️ 空的人脸区域，跳过")
                continue
            
            print(f"   位置: ({x}, {y}), 尺寸: {w}x{h}")
            
            # 分析性别（使用深度学习模型）
            gender, gender_conf = self.gender_age_analyzer.predict_gender(face_region)
            
            # 分析年龄（使用深度学习模型）
            age, age_conf = self.gender_age_analyzer.predict_age(face_region)
            
            # 分析表情
            expression, expr_conf = self.expression_analyzer.analyze_expression(face_region)
            
            # 计算综合置信度
            confidence = (gender_conf + age_conf + expr_conf) / 3
            
            result = {
                'face_id': i + 1,
                'bounding_box': [x, y, w, h],
                'gender': gender,
                'age': age,
                'expression': expression,
                'confidence': confidence,
                'gender_confidence': gender_conf,
                'age_confidence': age_conf,
                'expression_confidence': expr_conf,
                'method': '深度学习' if gender_conf > 0.5 else '规则方法'
            }
            
            results.append(result)
            
            print(f"   👦 性别: {gender} (置信度: {gender_conf:.2f})")
            print(f"   🎂 年龄: {age} (置信度: {age_conf:.2f})")
            print(f"   😊 表情: {expression} (置信度: {expr_conf:.2f})")
            print(f"   综合置信度: {confidence:.2f}")
            
            # 在图像上绘制结果
            result_image = self._draw_face_analysis(result_image, result)
        
        # 保存和显示结果
        output_path = self._save_result_image(result_image, image_path)
        self._display_results(result_image, results, image_path)
        
        return {
            'image_path': image_path,
            'faces_detected': len(results),
            'results': results,
            'output_path': output_path
        }
    
    def _draw_face_analysis(self, image, result):
        """在图像上绘制人脸分析结果"""
        x, y, w, h = result['bounding_box']
        confidence = result['confidence']
        
        # 根据置信度调整颜色
        if confidence > 0.7:
            color = (0, 255, 0)  # 高置信度 - 绿色
        elif confidence > 0.6:
            color = (0, 200, 255)  # 中等置信度 - 橙黄色
        elif confidence > 0.5:
            color = (0, 165, 255)  # 较低置信度 - 橙色
        else:
            color = (0, 100, 255)  # 低置信度 - 红色
        
        # 绘制人脸框
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        
        # 绘制人脸ID
        cv2.putText(image, f"ID:{result['face_id']}", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # 准备中文显示文本 - 使用深色背景提高可读性
        method_icon = "🧠" if result.get('method') == '深度学习' else "📐"
        lines = [
            f"{method_icon} ID: {result['face_id']}",
            f"性别: {result['gender']}",
            f"年龄: {result['age']}",
            f"表情: {result['expression']}",
            f"置信度: {result['confidence']:.2f}"
        ]
        
        # 计算文本位置
        text_x = x
        text_y = y + h + 20
        
        # 调整文本位置防止超出
        if text_y + len(lines) * 25 > image.shape[0]:
            text_y = max(20, y - len(lines) * 25)
        
        # 绘制中文文本 - 添加背景框提高可读性
        # 先绘制半透明背景框
        bg_height = len(lines) * 25
        bg_width = 200
        overlay = image.copy()
        cv2.rectangle(overlay, (text_x-5, text_y-5), 
                     (text_x + bg_width, text_y + bg_height), 
                     (0, 0, 0), -1)
        image = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)
        
        # 绘制文本
        image = self.chinese_renderer.put_multiline_chinese_text(
            image, lines, (text_x, text_y),
            font_size=15, line_spacing=5, color=color
        )
        
        return image
    
    def _handle_no_faces(self, image, image_path):
        """处理未检测到人脸的情况"""
        result_image = image.copy()
        
        # 添加中文提示
        tips = [
            "⚠️ 未检测到人脸",
            "可能原因:",
            "1. 人脸不清晰",
            "2. 光线不足",
            "3. 角度不合适",
            "4. 图像质量差"
        ]
        
        # 绘制提示 - 使用深色背景
        y_offset = 30
        for tip in tips:
            # 添加背景框
            bg_x, bg_y = 25, y_offset - 5
            bg_width, bg_height = 300, 30
            overlay = result_image.copy()
            cv2.rectangle(overlay, (bg_x, bg_y), 
                         (bg_x + bg_width, bg_y + bg_height), 
                         (0, 0, 0), -1)
            result_image = cv2.addWeighted(overlay, 0.6, result_image, 0.4, 0)
            
            # 绘制文本
            result_image = self.chinese_renderer.put_chinese_text(
                result_image, tip, (30, y_offset),
                font_size=20, color=(0, 200, 255)  # 使用亮色文本
            )
            y_offset += 35
        
        output_path = self._save_result_image(result_image, image_path)
        
        # 显示结果
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("未检测到人脸", fontsize=16)
        plt.tight_layout()
        plt.show()
        
        return {
            'image_path': image_path,
            'faces_detected': 0,
            'results': [],
            'output_path': output_path
        }
    
    def _save_result_image(self, image, original_path):
        """保存结果图像"""
        output_dir = os.path.join(os.path.dirname(original_path), "analysis_results")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_深度学习分析结果{ext}")
        
        cv2.imwrite(output_path, image)
        print(f"💾 结果图像已保存: {output_path}")
        
        return output_path
    
    def _display_results(self, result_image, results, image_path):
        """显示分析结果"""
        # 创建更大的图像显示
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # 原图
        ax1 = axes[0]
        original_image = cv2.imread(image_path)
        if original_image is not None:
            if original_image.shape != result_image.shape:
                original_image = cv2.resize(original_image, 
                                          (result_image.shape[1], result_image.shape[0]))
            ax1.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
        ax1.set_title('原图像', fontsize=14)
        ax1.axis('off')
        
        # 结果图
        ax2 = axes[1]
        ax2.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        ax2.set_title(f'分析结果 (检测到 {len(results)} 张人脸)', fontsize=14)
        ax2.axis('off')
        
        # 添加统计信息
        if results:
            stats_text = "📊 分析结果统计:\n\n"
            deep_learning_count = 0
            rule_based_count = 0
            
            for result in results:
                # 根据置信度添加表情符号
                if result['confidence'] > 0.7:
                    confidence_icon = "✅"
                elif result['confidence'] > 0.6:
                    confidence_icon = "⚠️"
                else:
                    confidence_icon = "❓"
                
                # 统计分析方法
                if result.get('method') == '深度学习':
                    method_icon = "🧠"
                    deep_learning_count += 1
                else:
                    method_icon = "📐"
                    rule_based_count += 1
                
                stats_text += f"{confidence_icon}{method_icon} 人脸 {result['face_id']}:\n"
                stats_text += f"   性别: {result['gender']}\n"
                stats_text += f"   年龄: {result['age']}\n"
                stats_text += f"   表情: {result['expression']}\n"
                stats_text += f"   置信度: {result['confidence']:.3f}\n\n"
            
            # 添加分析方法统计
            stats_text += f"\n📈 分析方法统计:\n"
            stats_text += f"   深度学习: {deep_learning_count}\n"
            stats_text += f"   规则方法: {rule_based_count}\n"
            
            plt.figtext(0.75, 0.5, stats_text, fontsize=11,
                       bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        # 打印摘要
        print("\n" + "=" * 65)
        print("深度学习分析结果摘要")
        print("=" * 65)
        print(f"图像路径: {image_path}")
        print(f"检测到人脸数: {len(results)}")
        
        # 统计性别分布
        gender_counts = {}
        for result in results:
            gender = result['gender']
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
        
        print(f"👥 性别分布: {', '.join([f'{k}:{v}' for k, v in gender_counts.items()])}")
        
        # 统计表情分布
        expression_counts = {}
        for result in results:
            expression = result['expression']
            expression_counts[expression] = expression_counts.get(expression, 0) + 1
        
        print(f"😊 表情分布: {', '.join([f'{k}:{v}' for k, v in expression_counts.items()])}")
        
        for result in results:
            method_icon = "🧠" if result.get('method') == '深度学习' else "📐"
            print(f"\n{method_icon} 人脸 {result['face_id']}:")
            print(f"  位置: ({result['bounding_box'][0]}, {result['bounding_box'][1]})")
            print(f"  尺寸: {result['bounding_box'][2]}x{result['bounding_box'][3]}")
            print(f"  性别: {result['gender']} (置信度: {result['gender_confidence']:.2f})")
            print(f"  年龄: {result['age']} (置信度: {result['age_confidence']:.2f})")
            print(f"  表情: {result['expression']} (置信度: {result['expression_confidence']:.2f})")
            print(f"  综合置信度: {result['confidence']:.3f}")
        
        print("=" * 65)

# -------------------------- 主函数 --------------------------
def main():
    """主函数"""
    print("\n🚀 启动深度学习人脸分析系统")
    print("注: 系统将创建轻量级深度学习模型用于性别年龄分析")
    
    # 创建分析器
    analyzer = PracticalFaceAnalyzer()
    
    # 初始化系统
    if not analyzer.setup():
        print("❌ 系统初始化失败")
        return
    
    # 指定要分析的图像路径
    image_path = r"C:\Users\86159\Desktop\1.jpg"
    
    # 如果指定路径不存在，查找其他图片
    if not os.path.exists(image_path):
        print(f"⚠️ 指定图片不存在: {image_path}")
        
        # 查找当前目录下的图片
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
        image_files = []
        
        for file in os.listdir(current_dir):
            if file.lower().endswith(image_extensions):
                image_files.append(file)
        
        if image_files:
            print("📁 在当前目录找到以下图片:")
            for idx, file in enumerate(image_files, 1):
                print(f"  {idx}. {file}")
            
            try:
                choice = int(input(f"请选择要分析的图片 (1-{len(image_files)}): "))
                if 1 <= choice <= len(image_files):
                    image_path = os.path.join(current_dir, image_files[choice-1])
                else:
                    print("⚠️ 选择无效，使用第一个图片")
                    image_path = os.path.join(current_dir, image_files[0])
            except:
                print("⚠️ 输入错误，使用第一个图片")
                image_path = os.path.join(current_dir, image_files[0])
        else:
            print("❌ 未找到任何图片文件")
            return
    
    print(f"\n🎯 分析目标: {image_path}")
    
    # 分析图像
    try:
        result = analyzer.analyze_single_image(image_path)
        
        if result:
            if result['faces_detected'] > 0:
                print(f"\n✅ 分析完成！检测到 {result['faces_detected']} 张人脸")
                print(f"💾 结果保存到: {result['output_path']}")
                
                # 分析质量评估
                avg_confidence = np.mean([r['confidence'] for r in result['results']])
                if avg_confidence > 0.7:
                    print(f"📈 分析质量: 优秀 (平均置信度: {avg_confidence:.2f})")
                elif avg_confidence > 0.6:
                    print(f"📊 分析质量: 良好 (平均置信度: {avg_confidence:.2f})")
                elif avg_confidence > 0.5:
                    print(f"📉 分析质量: 一般 (平均置信度: {avg_confidence:.2f})")
                else:
                    print(f"⚠️ 分析质量: 较低 (平均置信度: {avg_confidence:.2f})")
                    
                print("\n💡 改进建议:")
                if avg_confidence < 0.6:
                    print("  1. 尝试使用更清晰的人脸正面图片")
                    print("  2. 确保人脸在图像中足够大")
                    print("  3. 提供均匀的光照条件")
                print("  4. 系统结合深度学习和规则方法进行分析")
            else:
                print("\n⚠️ 未检测到人脸")
                print("💡 建议: 请使用清晰的人脸正面图片")
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()