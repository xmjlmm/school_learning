# import xml.etree.ElementTree as ET
# from os import getcwd

# sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes = ['cat']


# def convert_annotation(year, image_id, list_file):
#     in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
#     tree=ET.parse(in_file)
#     root = tree.getroot()

#     for obj in root.iter('object'):
#         difficult = obj.find('difficult').text
#         cls = obj.find('name').text
#         if cls not in classes or int(difficult)==1:
#             continue
#         cls_id = classes.index(cls)
#         xmlbox = obj.find('bndbox')
#         b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
#         list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

# wd = getcwd()

# for year, image_set in sets:
#     image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#     list_file = open('%s_%s.txt'%(year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
#         convert_annotation(year, image_id, list_file)
#         list_file.write('\n')
#     list_file.close()



import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
classes = ["cat"]

def convert_annotation(year, image_id, list_file):
    """转换标注文件函数 - 修复路径问题"""
    # 构建正确的注解文件路径
    xml_path = os.path.join('F:/data/VOC2007/Annotations', f'{image_id}.xml')
    
    try:
        in_file = open(xml_path)
        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), 
                 int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
            list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    except FileNotFoundError:
        print(f"警告: 注解文件未找到: {xml_path}")
    except Exception as e:
        print(f"处理注解文件时出错: {e}")

wd = getcwd()

for year, image_set in sets:
    # 读取ImageSets文件
    imageset_path = f'F:/data/VOC2007/ImageSets/Main/{image_set}.txt'
    
    try:
        with open(imageset_path, 'r') as f:
            lines = f.readlines()
        
        # 清理每行的内容，只保留纯文件名（不含路径和扩展名）
        image_ids = []
        for line in lines:
            line = line.strip()
            if line:  # 确保行不为空
                # 提取纯文件名（不含路径和扩展名）
                filename = os.path.basename(line)  # 去除路径
                filename = os.path.splitext(filename)[0]  # 去除扩展名
                image_ids.append(filename)
        
        # 创建输出文件
        output_file = f'{year}_{image_set}.txt'
        with open(output_file, 'w', encoding='utf-8') as list_file:
            for image_id in image_ids:
                # 写入图片路径（使用正确的绝对路径）
                img_path = f'F:/data/VOC2007/JPEGImages/{image_id}.jpg'
                list_file.write(img_path)
                
                # 转换并添加标注信息
                convert_annotation(year, image_id, list_file)
                list_file.write('\n')
        
        print(f'成功生成: {output_file}, 包含 {len(image_ids)} 个样本')
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {imageset_path}")
    except Exception as e:
        print(f"处理 {image_set} 集时出错: {e}")

print("所有文件生成完成！")