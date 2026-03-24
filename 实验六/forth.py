import os
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 使用交互式后端
import matplotlib.pyplot as plt
import warnings
from PIL import Image, ImageDraw, ImageFont
from collections import deque
warnings.filterwarnings('ignore')

print("=" * 60)
print("中文人脸图像分析系统 - 稳定增强版")
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
            draw.text((x, y), text, font=font, fill=color[::-1])  # BGR转RGB
            
            # 转换回OpenCV格式
            if len(image.shape) == 3 and image.shape[2] == 3:
                result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            else:
                result = np.array(pil_image)
            
            return result
            
        except Exception as e:
            print(f"绘制中文文本失败: {e}")
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

class RobustFaceAnalyzer:
    """鲁棒的人脸分析器 - 基于OpenCV"""
    
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self.chinese_renderer = ChineseTextRenderer()
        self.min_face_size = 40
        self.max_face_size = 400
        self.face_history = deque(maxlen=10)  # 人脸检测历史
        
    def setup(self):
        """初始化分析系统"""
        print("🔧 初始化人脸分析系统...")
        
        # 初始化OpenCV Haar级联检测器
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            print("✅ OpenCV人脸检测器初始化成功")
            return True
        except Exception as e:
            print(f"❌ 检测器初始化失败: {e}")
            return False
    
    def detect_faces_robust(self, image):
        """鲁棒的人脸检测方法"""
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
        
        # 如果没有检测到，尝试使用原始灰度图
        if len(faces) == 0:
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(self.min_face_size, self.min_face_size),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        
        return faces
    
    def analyze_face_features(self, face_region, face_position, image_size):
        """分析人脸特征 - 基于规则的方法"""
        height, width = face_region.shape[:2]
        
        # 性别分析
        gender, gender_conf = self._estimate_gender(face_region)
        
        # 年龄分析
        age, age_conf = self._estimate_age(face_region)
        
        # 表情分析
        expression, expr_conf = self._estimate_expression(face_region)
        
        # 计算综合置信度
        confidence = (gender_conf + age_conf + expr_conf) / 3
        
        return {
            'gender': gender,
            'age': age,
            'expression': expression,
            'gender_confidence': gender_conf,
            'age_confidence': age_conf,
            'expression_confidence': expr_conf,
            'overall_confidence': confidence
        }
    
    def _estimate_gender(self, face_img):
        """估计性别 - 基于面部特征"""
        try:
            if len(face_img.shape) == 3:
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_img
            
            height, width = face_img.shape[:2]
            
            # 面部宽高比特征
            aspect_ratio = width / height if height > 0 else 1.0
            
            # 下巴特征（通过下半部分分析）
            chin_region = face_img[int(height * 0.6):, :]
            
            # 眼睛检测（辅助判断）
            eyes = []
            if len(gray.shape) == 2 and self.eye_cascade:
                eyes = self.eye_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(20, 20)
                )
            
            # 综合判断
            gender_score = 0
            features_detected = 0
            
            # 特征1: 面部宽高比
            if aspect_ratio > 1.1:  # 男性通常脸更宽
                gender_score += 1
            elif aspect_ratio < 0.95:  # 女性通常脸更窄
                gender_score -= 1
            features_detected += 1
            
            # 特征2: 下巴宽度
            if chin_region.shape[0] > 0:
                chin_aspect = chin_region.shape[1] / chin_region.shape[0]
                if chin_aspect > 1.5:  # 宽下巴
                    gender_score += 1
                else:
                    gender_score -= 1
                features_detected += 1
            
            # 特征3: 眼睛大小和间距（如果检测到）
            if len(eyes) >= 2:
                # 计算眼睛间距相对脸宽的比例
                eye_spacing = abs(eyes[0][0] - eyes[1][0])
                eye_to_face_ratio = eye_spacing / width
                if eye_to_face_ratio > 0.3:  # 眼睛间距较大
                    gender_score -= 1
                features_detected += 1
            
            # 决定性别
            if features_detected > 0:
                if gender_score > 0:
                    return "男性", min(0.8, 0.5 + abs(gender_score) * 0.1)
                elif gender_score < 0:
                    return "女性", min(0.8, 0.5 + abs(gender_score) * 0.1)
            
            return "未知", 0.5
            
        except Exception as e:
            return "未知", 0.3
    
    def _estimate_age(self, face_img):
        """估计年龄 - 基于皮肤纹理"""
        try:
            if len(face_img.shape) == 3:
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_img
            
            height, width = gray.shape
            
            # 检查图像质量
            if height < 30 or width < 30:
                return "未知", 0.3
            
            # 1. 皮肤纹理分析 - 使用拉普拉斯算子
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 2. 边缘密度分析（皱纹检测）
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            
            # 3. 亮度均匀性分析
            brightness_mean = np.mean(gray)
            brightness_std = np.std(gray)
            
            # 综合判断
            age_score = 0
            features_detected = 0
            
            # 年轻人: 纹理光滑，边缘少，亮度均匀
            if laplacian_var < 150:  # 光滑皮肤
                age_score -= 2
            features_detected += 1
            
            if edge_density < 0.05:  # 皱纹少
                age_score -= 1
            features_detected += 1
            
            if brightness_std < 50:  # 亮度均匀
                age_score -= 1
            features_detected += 1
            
            # 年龄分类
            if features_detected > 0:
                if age_score <= -3:  # 非常年轻的特征
                    return "青年(20-35)", 0.7
                elif age_score <= -1:  # 年轻特征
                    return "青年(20-35)", 0.6
                elif age_score >= 1:  # 年长特征
                    if laplacian_var > 300:
                        return "老年(50+)", 0.6
                    else:
                        return "中年(36-50)", 0.6
                else:  # 中性特征
                    return "中年(36-50)", 0.5
            
            # 默认分类
            return "中年(36-50)", 0.5
            
        except Exception as e:
            return "未知", 0.3
    
    def _estimate_expression(self, face_img):
        """估计表情 - 基于嘴部和眼睛区域"""
        try:
            if len(face_img.shape) == 3:
                gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_img
            
            height, width = gray.shape
            
            # 嘴部区域（下半部分）
            mouth_region = gray[int(height * 0.6):, :]
            
            if mouth_region.shape[0] > 0:
                # 计算嘴部区域的水平梯度
                sobelx = cv2.Sobel(mouth_region, cv2.CV_64F, 1, 0, ksize=3)
                gradient_mean = np.mean(np.abs(sobelx))
                
                # 嘴部亮度变化（微笑时嘴角上扬）
                mouth_brightness = np.mean(mouth_region)
                mouth_contrast = np.std(mouth_region)
                
                # 判断表情
                if gradient_mean > 10 and mouth_contrast > 20:
                    return "微笑", 0.7
                elif gradient_mean < 5 and mouth_contrast < 10:
                    return "严肃", 0.6
                else:
                    return "中性", 0.5
            
            return "中性", 0.5
            
        except Exception as e:
            return "中性", 0.5
    
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
        
        # 调整图像尺寸（如果太大）
        max_dimension = 1200
        if max(original_height, original_width) > max_dimension:
            scale = max_dimension / max(original_height, original_width)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            image = cv2.resize(image, (new_width, new_height))
            print(f"🔄 图像尺寸调整: {original_width}x{original_height} -> {new_width}x{new_height}")
        
        print(f"✅ 图像加载成功, 尺寸: {image.shape[1]}x{image.shape[0]}")
        
        # 人脸检测
        faces = self.detect_faces_robust(image)
        
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
            
            if w <= 10 or h <= 10:
                print("⚠️ 人脸区域太小，跳过")
                continue
            
            # 提取人脸区域
            face_region = image[y:y+h, x:x+w]
            
            if face_region.size == 0:
                print("⚠️ 空的人脸区域，跳过")
                continue
            
            print(f"   位置: ({x}, {y}), 尺寸: {w}x{h}")
            
            # 分析人脸特征
            features = self.analyze_face_features(face_region, (x, y), image.shape)
            
            result = {
                'face_id': i + 1,
                'bounding_box': [x, y, w, h],
                'gender': features['gender'],
                'age': features['age'],
                'expression': features['expression'],
                'confidence': features['overall_confidence']
            }
            
            results.append(result)
            
            print(f"   👦 性别: {features['gender']} (置信度: {features['gender_confidence']:.2f})")
            print(f"   🎂 年龄: {features['age']} (置信度: {features['age_confidence']:.2f})")
            print(f"   😊 表情: {features['expression']} (置信度: {features['expression_confidence']:.2f})")
            
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
        elif confidence > 0.5:
            color = (0, 255, 255)  # 中等置信度 - 黄色
        else:
            color = (0, 165, 255)  # 低置信度 - 橙色
        
        # 绘制人脸框
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        
        # 绘制人脸ID
        cv2.putText(image, f"ID:{result['face_id']}", (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # 准备中文显示文本
        lines = [
            f"ID: {result['face_id']}",
            f"性别: {result['gender']}",
            f"年龄: {result['age']}",
            f"表情: {result['expression']}",
            f"置信度: {result['confidence']:.2f}"
        ]
        
        # 计算文本位置
        text_x = x
        text_y = y + h + 20
        
        # 如果文本会在图像底部超出，调整位置
        if text_y + len(lines) * 25 > image.shape[0]:
            text_y = y - len(lines) * 25
        
        # 绘制中文文本
        image = self.chinese_renderer.put_multiline_chinese_text(
            image, lines, (text_x, text_y),
            font_size=15, line_spacing=5, color=color
        )
        
        return image
    
    def _handle_no_faces(self, image, image_path):
        """处理未检测到人脸的情况"""
        print("⚠️ 未检测到人脸，显示原图")
        
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
        
        # 绘制提示
        y_offset = 30
        for tip in tips:
            result_image = self.chinese_renderer.put_chinese_text(
                result_image, tip, (30, y_offset),
                font_size=20, color=(0, 0, 255)
            )
            y_offset += 35
        
        output_path = self._save_result_image(result_image, image_path)
        
        # 显示结果
        self._display_single_image(result_image, "未检测到人脸")
        
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
        output_path = os.path.join(output_dir, f"{name}_鲁棒分析结果{ext}")
        
        cv2.imwrite(output_path, image)
        print(f"💾 结果图像已保存: {output_path}")
        
        return output_path
    
    def _display_single_image(self, image, title):
        """显示单张图像"""
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(title, fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def _display_results(self, result_image, results, image_path):
        """显示分析结果"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 读取原图
        original_image = cv2.imread(image_path)
        if original_image is not None:
            # 调整原图尺寸以匹配结果图
            if original_image.shape != result_image.shape:
                original_image = cv2.resize(original_image, 
                                          (result_image.shape[1], result_image.shape[0]))
            
            axes[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            axes[0].set_title('原图像')
            axes[0].axis('off')
        
        # 显示结果图
        axes[1].imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        axes[1].set_title(f'分析结果 (检测到 {len(results)} 张人脸)')
        axes[1].axis('off')
        
        # 添加统计信息
        if results:
            stats_text = "分析结果统计:\n\n"
            for result in results:
                stats_text += f"人脸 {result['face_id']}:\n"
                stats_text += f"  位置: ({result['bounding_box'][0]}, {result['bounding_box'][1]})\n"
                stats_text += f"  尺寸: {result['bounding_box'][2]}x{result['bounding_box'][3]}\n"
                stats_text += f"  性别: {result['gender']}\n"
                stats_text += f"  年龄: {result['age']}\n"
                stats_text += f"  表情: {result['expression']}\n"
                stats_text += f"  置信度: {result['confidence']:.3f}\n\n"
            
            plt.figtext(0.02, 0.5, stats_text, fontsize=10,
                       bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        
        plt.tight_layout()
        plt.show()
        
        # 打印摘要
        print("\n" + "=" * 60)
        print("鲁棒分析结果摘要")
        print("=" * 60)
        print(f"图像路径: {image_path}")
        print(f"检测到人脸数: {len(results)}")
        
        for result in results:
            print(f"\n人脸 {result['face_id']}:")
            print(f"  位置: {result['bounding_box'][0:2]}")
            print(f"  尺寸: {result['bounding_box'][2]}x{result['bounding_box'][3]}")
            print(f"  性别: {result['gender']}")
            print(f"  年龄: {result['age']}")
            print(f"  表情: {result['expression']}")
            print(f"  置信度: {result['confidence']:.3f}")
        
        print("=" * 60)

# -------------------------- 主函数 --------------------------
def main():
    """主函数"""
    print("\n🚀 启动鲁棒人脸分析系统")
    
    # 创建分析器
    analyzer = RobustFaceAnalyzer()
    
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
            # 尝试使用示例图片
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
            else:
                print("\n⚠️ 未检测到人脸")
                print("💡 建议: 请使用清晰的人脸正面图片")
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()