import os
import cv2
import numpy as np
import tensorflow as tf
from mtcnn import MTCNN
import matplotlib
matplotlib.use('TkAgg')  # 使用交互式后端
import matplotlib.pyplot as plt
import warnings
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
warnings.filterwarnings('ignore')

print("=" * 60)
print("中文人脸图像分析系统")
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
                os.path.join(system_fonts_dir, "simfang.ttf"),  # 仿宋
            ]
        else:  # Linux/Mac
            possible_fonts = [
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",  # 文泉驿微米黑
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Noto字体
                "/System/Library/Fonts/PingFang.ttc",  # macOS 苹方字体
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
            # 确保输入是有效的
            if image is None or len(image.shape) < 2:
                return image
            
            # 确保颜色格式正确
            if isinstance(color, tuple) and len(color) == 3:
                # OpenCV使用BGR，PIL使用RGB
                color_rgb = (color[2], color[1], color[0])
            else:
                color_rgb = (0, 255, 0)  # 默认绿色
            
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
            draw.text((x, y), text, font=font, fill=color_rgb)
            
            # 转换回OpenCV格式
            if len(image.shape) == 3 and image.shape[2] == 3:
                result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            else:
                result = np.array(pil_image)
            
            return result
            
        except Exception as e:
            print(f"绘制中文文本失败: {e}")
            # 如果失败，使用OpenCV的英文文本
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

class RealFaceAnalyzer:
    def __init__(self):
        self.detector = None
        self.model = None
        self.chinese_renderer = ChineseTextRenderer()
        self.setup_complete = False
        
    def setup(self):
        """初始化分析系统"""
        print("🔧 初始化人脸分析系统...")
        
        # 初始化MTCNN人脸检测器
        try:
            self.detector = MTCNN()
            print("✅ MTCNN检测器初始化成功")
        except Exception as e:
            print(f"❌ MTCNN初始化失败: {e}")
            return False
        
        # 初始化简化的人脸属性分析模型
        self.model = self._build_simple_model()
        print("✅ 人脸属性分析模型就绪")
        
        self.setup_complete = True
        print("✅ 系统初始化完成")
        return True
    
    def _build_simple_model(self):
        """构建简化的人脸属性分析模型（基于规则）"""
        class SimpleRuleBasedModel:
            def __init__(self):
                self.age_groups = ["儿童(0-12)", "青少年(13-19)", "青年(20-35)", "中年(36-50)", "老年(50+)"]
                self.gender_labels = ["男性", "女性"]
                self.expression_labels = ["中性", "微笑", "大笑", "严肃"]
            
            def analyze_face_features(self, face_img, keypoints):
                """基于面部特征的简单分析"""
                try:
                    # 转换为灰度图进行分析
                    if len(face_img.shape) == 3:
                        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    else:
                        gray_face = face_img
                    
                    # 提取关键点（如果可用）
                    if keypoints:
                        # 基于关键点距离的比例分析
                        gender = self._estimate_gender(keypoints)
                        age = self._estimate_age(face_img, keypoints)
                        expression = self._estimate_expression(keypoints)
                    else:
                        # 如果没有关键点，使用默认值
                        gender = "未知"
                        age = "未知"
                        expression = "未知"
                    
                    return gender, age, expression
                    
                except Exception as e:
                    print(f"特征分析错误: {e}")
                    return "分析失败", "分析失败", "分析失败"
            
            def _estimate_gender(self, keypoints):
                """基于面部特征估计性别"""
                try:
                    # 简单的性别估计逻辑（基于面部比例）
                    if 'left_eye' in keypoints and 'right_eye' in keypoints:
                        left_eye = keypoints['left_eye']
                        right_eye = keypoints['right_eye']
                        eye_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
                        
                        if 'nose' in keypoints and 'mouth_left' in keypoints:
                            nose = keypoints['nose']
                            mouth_left = keypoints['mouth_left']
                            vertical_dist = np.linalg.norm(np.array(nose) - np.array(mouth_left))
                            
                            if vertical_dist > 0:
                                ratio = eye_distance / vertical_dist
                                # 男性通常有更宽的面部特征
                                return "男性" if ratio > 1.2 else "女性"
                    
                    return "未知"
                except:
                    return "未知"
            
            def _estimate_age(self, face_img, keypoints):
                """基于皮肤纹理和面部特征估计年龄"""
                try:
                    # 转换为灰度图进行纹理分析
                    if len(face_img.shape) == 3:
                        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    else:
                        gray = face_img
                    
                    # 计算图像清晰度（拉普拉斯方差）
                    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                    
                    # 基于纹理粗糙度的简单年龄估计
                    if laplacian_var > 500:
                        return "青年(20-35)"
                    elif laplacian_var > 200:
                        return "中年(36-50)"
                    elif laplacian_var > 100:
                        return "老年(50+)"
                    else:
                        return "未知"
                        
                except:
                    return "未知"
            
            def _estimate_expression(self, keypoints):
                """基于嘴部关键点估计表情"""
                try:
                    if 'mouth_left' in keypoints and 'mouth_right' in keypoints:
                        mouth_left = keypoints['mouth_left']
                        mouth_right = keypoints['mouth_right']
                        
                        if 'nose' in keypoints:
                            nose = keypoints['nose']
                            # 计算嘴部弯曲程度（简单微笑检测）
                            mouth_center_y = (mouth_left[1] + mouth_right[1]) / 2
                            nose_mouth_dist = mouth_center_y - nose[1]
                            
                            if nose_mouth_dist > 0:
                                return "微笑" if nose_mouth_dist > 15 else "中性"
                    
                    return "未知"
                except:
                    return "未知"
        
        return SimpleRuleBasedModel()
    
    def analyze_single_image(self, image_path):
        """分析单张人脸图像"""
        if not self.setup_complete:
            print("❌ 请先调用setup()方法初始化系统")
            return None
        
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
        
        print(f"✅ 图像加载成功, 尺寸: {image.shape[1]}x{image.shape[0]}")
        
        # 人脸检测
        try:
            # 转换到RGB格式（MTCNN需要）
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces = self.detector.detect_faces(rgb_image)
            print(f"🔍 检测到 {len(faces)} 张人脸")
        except Exception as e:
            print(f"❌ 人脸检测失败: {e}")
            faces = []
        
        if not faces:
            print("⚠️ 未检测到人脸，尝试使用备选检测方法...")
            faces = self._fallback_face_detection(image)
            if not faces:
                print("❌ 所有检测方法均未检测到人脸")
                return self._display_no_face_result(image, image_path)
        
        # 分析每张检测到的人脸
        results = []
        result_image = image.copy()
        
        for i, face in enumerate(faces):
            print(f"\n👤 分析第 {i+1} 张人脸...")
            
            # 提取人脸边界框
            bounding_box = face['box']
            x, y, w, h = bounding_box
            
            # 确保坐标不越界
            x = max(0, x)
            y = max(0, y)
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)
            
            if w <= 0 or h <= 0:
                print("⚠️ 无效的人脸区域，跳过")
                continue
            
            # 提取人脸区域
            face_region = image[y:y+h, x:x+w]
            
            if face_region.size == 0:
                print("⚠️ 空的人脸区域，跳过")
                continue
            
            # 获取关键点
            keypoints = face.get('keypoints', {})
            confidence = face.get('confidence', 0.0)
            
            print(f"   位置: ({x}, {y}), 尺寸: {w}x{h}, 置信度: {confidence:.3f}")
            
            # 分析人脸属性
            gender, age, expression = self.model.analyze_face_features(face_region, keypoints)
            
            result = {
                'face_id': i + 1,
                'bounding_box': [x, y, w, h],
                'gender': gender,
                'age': age,
                'expression': expression,
                'confidence': confidence
            }
            
            results.append(result)
            
            print(f"   👦 性别: {gender}")
            print(f"   🎂 年龄: {age}")
            print(f"   😊 表情: {expression}")
            
            # 在图像上绘制结果
            result_image = self._draw_face_result(result_image, result, keypoints)
        
        # 保存和显示结果
        output_path = self._save_result_image(result_image, image_path)
        self._display_results(result_image, results, image_path)
        
        return {
            'image_path': image_path,
            'faces_detected': len(results),
            'results': results,
            'output_path': output_path
        }
    
    def _fallback_face_detection(self, image):
        """备选人脸检测方法（使用OpenCV Haar级联）"""
        try:
            # 加载OpenCV的人脸检测器
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
            
            results = []
            for (x, y, w, h) in faces:
                # 创建模拟的关键点
                results.append({
                    'box': [x, y, w, h],
                    'confidence': 0.7,  # 默认置信度
                    'keypoints': {
                        'left_eye': (x + w//3, y + h//3),
                        'right_eye': (x + 2*w//3, y + h//3),
                        'nose': (x + w//2, y + h//2),
                        'mouth_left': (x + w//3, y + 2*h//3),
                        'mouth_right': (x + 2*w//3, y + 2*h//3)
                    }
                })
            
            if results:
                print(f"🔄 Haar级联检测器检测到 {len(results)} 张人脸")
            
            return results
        except Exception as e:
            print(f"❌ 备选检测方法失败: {e}")
            return []
    
    def _draw_face_result(self, image, result, keypoints):
        """在图像上绘制人脸分析结果（使用中文）"""
        x, y, w, h = result['bounding_box']
        
        # 绘制人脸边界框
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        
        # 绘制关键点（如果存在）
        for point_name, point in keypoints.items():
            cv2.circle(image, point, 3, (255, 0, 0), -1)  # 蓝色关键点
        
        # 准备显示文本
        label = f"{result['gender']}, {result['age']}, {result['expression']}"
        confidence_text = f"置信度: {result['confidence']:.3f}"
        
        # 计算文本位置（确保在图像内）
        text_y = y - 20 if y - 20 > 20 else y + h + 30
        
        # 使用中文渲染器绘制文本
        image = self.chinese_renderer.put_chinese_text(
            image, label, (x, text_y), font_size=10, color=color
        )
        
        # 绘制置信度文本（如果空间足够）
        if text_y + 25 < image.shape[0]:
            image = self.chinese_renderer.put_chinese_text(
                image, confidence_text, (x, text_y + 25), 
                font_size=15, color=(255, 255, 255)
            )
        
        return image
    
    def _display_no_face_result(self, image, image_path):
        """处理未检测到人脸的情况（使用中文）"""
        print("⚠️ 未检测到人脸，显示原图")
        
        # 创建结果图像
        result_image = image.copy()
        
        # 添加中文提示文本
        result_image = self.chinese_renderer.put_chinese_text(
            result_image, "未检测到人脸", (50, 50), 
            font_size=10, color=(0, 0, 255)
        )
        
        # 保存结果
        output_path = self._save_result_image(result_image, image_path)
        
        # 显示结果
        self._display_single_image(result_image, image_path, "未检测到人脸")
        
        return {
            'image_path': image_path,
            'faces_detected': 0,
            'results': [],
            'output_path': output_path
        }
    
    def _display_single_image(self, image, image_path, title=None):
        """显示单张图像"""
        if title is None:
            title = os.path.basename(image_path)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(title, fontproperties=self._get_matplotlib_chinese_font())
        plt.tight_layout()
        plt.show()
    
    def _get_matplotlib_chinese_font(self):
        """获取matplotlib的中文字体"""
        from matplotlib.font_manager import FontProperties
        
        # 查找中文字体
        if os.name == 'nt':  # Windows
            font_paths = [
                r"C:\Windows\Fonts\msyh.ttc",  # 微软雅黑
                r"C:\Windows\Fonts\simhei.ttf",  # 黑体
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                "/System/Library/Fonts/PingFang.ttc",
            ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                return FontProperties(fname=font_path)
        
        # 如果找不到中文字体，返回默认字体
        return FontProperties()
    
    def _save_result_image(self, image, original_path):
        """保存结果图像"""
        # 创建输出目录
        output_dir = os.path.join(os.path.dirname(original_path), "analysis_results")
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成输出路径
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_中文分析结果{ext}")
        
        # 保存图像
        cv2.imwrite(output_path, image)
        print(f"💾 结果图像已保存: {output_path}")
        
        return output_path
    
    def _display_results(self, result_image, results, image_path):
        """显示分析结果（使用中文）"""
        # 创建显示图像
        display_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 显示原图（左侧）
        original_image = cv2.imread(image_path)
        if original_image is not None:
            ax1.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            ax1.set_title('原图像', fontproperties=self._get_matplotlib_chinese_font())
            ax1.axis('off')
        
        # 显示结果图（右侧）
        ax2.imshow(display_image)
        ax2.set_title(f'分析结果 (检测到 {len(results)} 张人脸)', 
                     fontproperties=self._get_matplotlib_chinese_font())
        ax2.axis('off')
        
        # 添加中文结果统计
        if results:
            stats_text = "分析结果统计:\n\n"
            for i, result in enumerate(results):
                stats_text += f"人脸 {i+1}:\n"
                stats_text += f"  性别: {result['gender']}\n"
                stats_text += f"  年龄: {result['age']}\n"
                stats_text += f"  表情: {result['expression']}\n"
                stats_text += f"  置信度: {result['confidence']:.3f}\n\n"
            
            # 在图像右侧添加文本
            plt.figtext(0.75, 0.5, stats_text, fontsize=10, 
                       fontproperties=self._get_matplotlib_chinese_font(),
                       bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        
        plt.tight_layout()
        plt.show()
        
        # 打印详细结果
        print("\n" + "=" * 50)
        print("分析结果摘要")
        print("=" * 50)
        print(f"图像路径: {image_path}")
        print(f"检测到人脸数: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"\n人脸 {i+1}:")
            print(f"  位置: {result['bounding_box']}")
            print(f"  性别: {result['gender']}")
            print(f"  年龄: {result['age']}")
            print(f"  表情: {result['expression']}")
            print(f"  置信度: {result['confidence']:.3f}")
        
        print("=" * 50)

# -------------------------- 主函数 --------------------------
def main():
    """主函数 - 分析指定图像"""
    # 创建分析器
    analyzer = RealFaceAnalyzer()
    
    # 初始化系统
    if not analyzer.setup():
        print("❌ 系统初始化失败")
        return
    
    # 指定要分析的图像路径
    image_path = r"C:\Users\86159\Desktop\1.jpg"
    
    # 如果指定路径不存在，尝试使用默认图片
    if not os.path.exists(image_path):
        print(f"⚠️ 指定图片不存在: {image_path}")
        # 尝试在当前目录查找图片
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_files = [f for f in os.listdir(current_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            image_path = os.path.join(current_dir, image_files[0])
            print(f"🔄 使用找到的图片: {image_path}")
        else:
            print("❌ 未找到任何图片文件")
            return
    
    print(f"🎯 目标图像: {image_path}")
    
    # 分析图像
    try:
        result = analyzer.analyze_single_image(image_path)
        
        if result and result['faces_detected'] > 0:
            print("\n✅ 分析完成！")
        else:
            print("\n⚠️  分析完成，但未检测到人脸")
            
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()