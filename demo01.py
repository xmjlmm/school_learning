# import os

# def convert_train_txt():
#     # 原始文件路径
#     original_file = r'F:\PycharmProjects\pythonProject\大四上\专项课程\VOC2007\ImageSets\Main\train.txt'
#     # 备份原文件（可选）
#     backup_file = original_file + '.backup'
#     # 图片目录路径
#     jpegimages_path = r'F:\PycharmProjects\pythonProject\大四上\专项课程\VOC2007\JPEGImages'
    
#     # 读取原始文件
#     with open(original_file, 'r') as f:
#         lines = f.readlines()
    
#     print(f"原始文件行数: {len(lines)}")
    
#     # 转换格式
#     new_lines = []
#     for i, line in enumerate(lines):
#         line = line.strip()
#         if not line:  # 跳过空行
#             continue
            
#         # 分割每行的数字（可能有空格或制表符分隔）
#         parts = line.split()
#         if len(parts) >= 2:
#             # 取第二个数字作为图片ID
#             image_id = parts[1]
#             # 构建完整图片路径
#             image_path = os.path.join(jpegimages_path, f"{image_id}.jpg")
#             new_lines.append(image_path + '\n')
#             if i < 5:  # 显示前5个转换示例
#                 print(f"转换示例: '{line}' -> '{image_path}'")
#         else:
#             print(f"警告: 第{i+1}行格式异常: '{line}'")
    
#     # 备份原文件（重命名）
#     if os.path.exists(original_file):
#         os.rename(original_file, backup_file)
#         print(f"已备份原文件为: {backup_file}")
    
#     # 写入转换后的文件
#     with open(original_file, 'w') as f:
#         f.writelines(new_lines)
    
#     print(f"转换完成! 共处理 {len(new_lines)} 行")
#     print(f"新文件已保存到: {original_file}")

# def verify_conversion():
#     """验证转换结果"""
#     train_txt_path = r'F:\PycharmProjects\pythonProject\大四上\专项课程\VOC2007\ImageSets\Main\train.txt'
#     jpegimages_path = r'F:\PycharmProjects\pythonProject\大四上\专项课程\VOC2007\JPEGImages'
    
#     print("\n验证转换结果:")
#     with open(train_txt_path, 'r') as f:
#         lines = f.readlines()
    
#     # 检查前几条路径对应的图片文件是否存在
#     existing_count = 0
#     for i, line in enumerate(lines[:10]):  # 检查前10个文件
#         image_path = line.strip()
#         if os.path.exists(image_path):
#             status = "存在 ✓"
#             existing_count += 1
#         else:
#             status = "不存在 ✗"
#         print(f"{image_path} -> {status}")
    
#     print(f"\n前10个文件中，{existing_count}个文件存在，{10-existing_count}个文件不存在")
    
#     if existing_count == 0:
#         print("警告: 未找到任何图片文件，请检查JPEGImages路径是否正确")

# if __name__ == "__main__":
#     # 执行转换
#     convert_train_txt()
    
#     # 验证结果
#     verify_conversion()



from PIL import Image, ImageDraw
import os

def draw_cat_face_box(image_path, output_path=None):
    """
    在猫脸位置绘制红色方框
    基于图片描述估计猫脸位置
    """
    try:
        # 打开图片
        image = Image.open(image_path)
        width, height = image.size
        
        print(f"图片尺寸: {width}x{height}")
        
        # 创建绘图对象
        draw = ImageDraw.Draw(image)
        
        # 基于描述估算猫脸位置
        # 猫脸在画面中心偏右，因此x坐标稍大于宽度的一半
        face_center_x = width * 0.55  # 中心偏右
        face_center_y = height * 0.5  # 垂直居中
        
        # 估算猫脸大小（基于图片尺寸的比例）
        face_width = width * 0.25  # 脸宽约为图片宽度的25%
        face_height = height * 0.2  # 脸高约为图片高度的20%
        
        # 计算方框坐标
        x1 = int(face_center_x - face_width / 2)
        y1 = int(face_center_y - face_height / 2)
        x2 = int(face_center_x + face_width / 2)
        y2 = int(face_center_y + face_height / 2)
        
        # 确保坐标不超出图片边界
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)
        
        # 绘制红色方框
        box_color = (255, 0, 0)  # 红色
        box_width = 3  # 线宽
        
        draw.rectangle([x1, y1, x2, y2], outline=box_color, width=box_width)
        
        # 添加标签
        label = "Cat Face"
        try:
            # 尝试加载字体
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        if font:
            # 获取文本尺寸
            try:
                bbox = draw.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                try:
                    text_width, text_height = draw.textsize(label, font=font)
                except:
                    text_width = len(label) * 10
                    text_height = 20
        else:
            text_width = len(label) * 10
            text_height = 20
        
        # 标签位置（在方框上方）
        label_x = x1
        label_y = y1 - text_height - 10
        
        # 如果标签超出图片上边界，放在方框内部
        if label_y < 0:
            label_y = y1 + 5
        
        # 绘制标签背景
        draw.rectangle([label_x, label_y, label_x + text_width, label_y + text_height], 
                      fill=box_color)
        
        # 绘制标签文字
        if font:
            draw.text((label_x, label_y), label, fill=(255, 255, 255), font=font)
        else:
            draw.text((label_x, label_y), label, fill=(255, 255, 255))
        
        print(f"已绘制红色方框: 位置({x1}, {y1}, {x2}, {y2})")
        
        # 保存或显示结果
        if output_path:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            image.save(output_path)
            print(f"结果已保存至: {output_path}")
        
        # 显示图片
        image.show()
        
        return image
        
    except Exception as e:
        print(f"处理图片时出错: {e}")
        return None

def adjust_box_position(image_path, output_path, x_center=0.55, y_center=0.5, width_ratio=0.25, height_ratio=0.2):
    """
    可调整方框位置的版本
    参数说明:
    - x_center: 方框中心水平位置 (0-1, 0=最左, 1=最右)
    - y_center: 方框中心垂直位置 (0-1, 0=最上, 1=最下)
    - width_ratio: 方框宽度与图片宽度比例
    - height_ratio: 方框高度与图片高度比例
    """
    try:
        image = Image.open(image_path)
        width, height = image.size
        draw = ImageDraw.Draw(image)
        
        # 计算方框坐标
        face_center_x = width * x_center
        face_center_y = height * y_center
        face_width = width * width_ratio
        face_height = height * height_ratio
        
        x1 = int(face_center_x - face_width / 2)
        y1 = int(face_center_y - face_height / 2)
        x2 = int(face_center_x + face_width / 2)
        y2 = int(face_center_y + face_height / 2)
        
        # 确保坐标有效
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)
        
        # 绘制红色方框
        box_color = (255, 0, 0)
        draw.rectangle([x1, y1, x2, y2], outline=box_color, width=3)
        
        # 添加标签
        label = "Cat Face"
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            bbox = draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            font = None
            text_width = len(label) * 10
            text_height = 20
        
        label_x = x1
        label_y = y1 - text_height - 10
        if label_y < 0:
            label_y = y1 + 5
        
        draw.rectangle([label_x, label_y, label_x + text_width, label_y + text_height], 
                      fill=box_color)
        
        if font:
            draw.text((label_x, label_y), label, fill=(255, 255, 255), font=font)
        else:
            draw.text((label_x, label_y), label, fill=(255, 255, 255))
        
        print(f"调整后方框位置: ({x1}, {y1}, {x2}, {y2})")
        
        if output_path:
            image.save(output_path)
            print(f"结果已保存至: {output_path}")
        
        image.show()
        return image
        
    except Exception as e:
        print(f"调整位置时出错: {e}")
        return None

def main():
    """主函数：在猫脸位置绘制红色方框"""
    # 请将路径替换为您的实际图片路径
    image_path = "F:/data/VOC2007/test/60.jpg"  # 替换为您的图片路径
    
    if not os.path.exists(image_path):
        print(f"图片不存在: {image_path}")
        print("请将image_path替换为您的实际图片路径")
        return
    
    print("=" * 50)
    print("在猫脸位置绘制红色方框")
    print("=" * 50)
    
    # 方法1: 使用默认位置
    print("\n1. 使用默认位置绘制:")
    result1 = draw_cat_face_box(image_path, "cat_face_default.jpg")
    
    # 方法2: 尝试不同的位置参数
    print("\n2. 尝试调整位置:")
    positions = [
        (0.55, 0.5, 0.25, 0.2),   # 默认：中心偏右
        (0.6, 0.5, 0.2, 0.15),     # 更偏右，稍小
        (0.5, 0.5, 0.3, 0.25),     # 居中，稍大
    ]
    
    for i, (x, y, w, h) in enumerate(positions):
        print(f"尝试位置 {i+1}: x_center={x}, y_center={y}")
        output_path = f"cat_face_adjust_{i+1}.jpg"
        adjust_box_position(image_path, output_path, x, y, w, h)
    
    print("\n绘制完成!")
    print("如果方框位置不准确，您可以:")
    print("1. 调整adjust_box_position函数的参数")
    print("2. 或使用图像编辑软件手动调整坐标")

if __name__ == "__main__":
    main()