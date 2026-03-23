import torch
import torch.nn as nn
import cv2
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import timm
from facenet_pytorch import MTCNN
import matplotlib.pyplot as plt

class CustomSwinModel(nn.Module):
    def __init__(self, num_genders=2, num_ages=10, num_expressions=7):
        super(CustomSwinModel, self).__init__()
        
        # 使用与权重文件匹配的Swin Transformer架构
        self.backbone = timm.create_model('swin_small_patch4_window7_224', 
                                         pretrained=False, num_classes=0)
        
        # 根据权重文件中的结构添加任务头
        feature_dim = 768  # Swin Small的特征维度
        
        # 年龄预测头（回归任务）
        self.age_predictor = nn.Sequential(
            nn.Linear(feature_dim, 384),
            nn.ReLU(),
            nn.Linear(384, 192),
            nn.ReLU(),
            nn.Linear(192, 1)  # 回归任务，输出1个值
        )
        
        # 性别分类头
        self.gender_classifier = nn.Sequential(
            nn.Linear(feature_dim, 384),
            nn.ReLU(),
            nn.Linear(384, 192),
            nn.ReLU(),
            nn.Linear(192, num_genders)
        )
        
        # 表情分类头
        self.expression_classifier = nn.Sequential(
            nn.Linear(feature_dim, 384),
            nn.ReLU(),
            nn.Linear(384, 192),
            nn.ReLU(),
            nn.Linear(192, num_expressions)
        )

    def forward(self, x):
        features = self.backbone(x)
        
        # 年龄预测（回归）
        age_out = self.age_predictor(features)
        
        # 性别分类
        gender_out = self.gender_classifier(features)
        
        # 表情分类
        expression_out = self.expression_classifier(features)
        
        return gender_out, age_out, expression_out

def load_and_explore_model(model_path):
    """加载并探索模型结构"""
    print("正在加载模型...")
    checkpoint = torch.load(model_path, map_location='cpu')
    
    # 探索模型结构
    if isinstance(checkpoint, dict):
        if 'model' in checkpoint:
            state_dict = checkpoint['model']
            print("模型包含在'model'键中")
        else:
            state_dict = checkpoint
            print("直接加载状态字典")
    else:
        state_dict = checkpoint.state_dict()
        print("加载完整模型实例")
    
    # 打印关键层信息
    print("\n模型关键层信息:")
    for key in list(state_dict.keys())[:10]:
        print(f"  {key}: {state_dict[key].shape}")
    
    # 特别关注输出层
    print("\n搜索输出层信息:")
    output_keys = [key for key in state_dict.keys() if any(x in key for x in ['head', 'classifier', 'fc', 'predictor'])]
    for key in output_keys:
        print(f"  {key}: {state_dict[key].shape}")
    
    return state_dict

def initialize_model(model_path, device):
    """初始化模型并加载权重"""
    # 先探索模型结构以确定输出维度
    state_dict = load_and_explore_model(model_path)
    
    # 根据权重文件中的分类器输出维度确定任务参数
    num_genders = 2
    num_ages = 1  # 回归任务，输出1个值
    num_expressions = 7
    
    # 查找分类器的输出维度
    for key in state_dict.keys():
        if 'classifier.fc.weight' in key:
            num_genders = state_dict[key].shape[0]
            print(f"检测到性别分类器输出维度: {num_genders}")
        elif 'predictor.fc.weight' in key:
            # 年龄可能是回归任务，输出维度为1
            num_ages = state_dict[key].shape[0]
            print(f"检测到年龄预测器输出维度: {num_ages}")
    
    # 创建模型实例
    model = CustomSwinModel(
        num_genders=num_genders,
        num_ages=num_ages,
        num_expressions=num_expressions
    )
    
    # 手动处理权重加载，移除不匹配的键
    print("\n处理权重加载...")
    model_dict = model.state_dict()
    
    # 过滤掉不匹配的键
    pretrained_dict = {}
    for k, v in state_dict.items():
        # 只加载backbone和匹配的头部权重
        if k in model_dict and model_dict[k].shape == v.shape:
            pretrained_dict[k] = v
        else:
            print(f"跳过不匹配的层: {k}")
    
    # 加载过滤后的权重
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)
    
    model.to(device)
    model.eval()
    print("模型权重加载成功!")
    
    return model, num_genders, num_ages, num_expressions

def setup_transforms():
    """设置图像预处理变换"""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

def predict_image_attributes(image_path, model_path):
    """主函数：预测图片中所有人头的属性"""
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    # 初始化模型
    model, num_genders, num_ages, num_expressions = initialize_model(model_path, device)
    preprocess = setup_transforms()
    
    # 初始化MTCNN人脸检测器
    mtcnn = MTCNN(keep_all=True, device=device)
    
    # 定义标签
    gender_labels = ['Male', 'Female'][:num_genders]
    
    # 年龄处理：如果是回归任务，需要映射到年龄段
    age_ranges = ['0-10', '11-20', '21-30', '31-40', '41-50', 
                 '51-60', '61-70', '71-80', '81-90', '90+']
    
    expression_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 
                        'Sad', 'Surprise', 'Neutral'][:num_expressions]
    
    # 加载图像
    print(f"\n正在处理图像: {image_path}")
    image = Image.open(image_path).convert('RGB')
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 人脸检测
    print("进行人脸检测...")
    boxes, probs = mtcnn.detect(image)
    
    results = []
    if boxes is not None:
        print(f"检测到 {len(boxes)} 个人脸")
        
        for i, (box, prob) in enumerate(zip(boxes, probs)):
            if prob is None or prob < 0.9:  # 置信度阈值
                continue
                
            # 提取人脸区域
            x1, y1, x2, y2 = [int(coord) for coord in box]
            face_region = image.crop((x1, y1, x2, y2))
            
            # 预处理
            input_tensor = preprocess(face_region).unsqueeze(0).to(device)
            
            # 预测
            with torch.no_grad():
                gender_logits, age_out, expression_logits = model(input_tensor)
            
            # 解析性别结果
            gender_probs = torch.softmax(gender_logits, dim=1)
            gender_idx = torch.argmax(gender_probs, dim=1).item()
            gender_conf = gender_probs[0][gender_idx].item()
            
            # 解析年龄结果
            if num_ages == 1:  # 回归任务
                age_pred = max(0, min(100, int(age_out.item())))  # 限制在0-100岁
                # 映射到年龄段
                age_range_idx = min(age_pred // 10, len(age_ranges) - 1)
                age_label = age_ranges[age_range_idx]
                age_conf = 0.9  # 回归任务没有传统置信度
            else:  # 分类任务
                age_probs = torch.softmax(age_out, dim=1)
                age_idx = torch.argmax(age_probs, dim=1).item()
                age_label = age_ranges[age_idx] if age_idx < len(age_ranges) else "Unknown"
                age_conf = age_probs[0][age_idx].item()
            
            # 解析表情结果
            expression_probs = torch.softmax(expression_logits, dim=1)
            expression_idx = torch.argmax(expression_probs, dim=1).item()
            expression_conf = expression_probs[0][expression_idx].item()
            
            # 存储结果
            result = {
                'face_id': i + 1,
                'box': [x1, y1, x2, y2],
                'gender': gender_labels[gender_idx],
                'gender_confidence': gender_conf,
                'age': age_label,
                'age_confidence': age_conf,
                'expression': expression_labels[expression_idx],
                'expression_confidence': expression_conf
            }
            results.append(result)
            
            # 在图像上绘制结果
            label = f"Face {i+1}: {gender_labels[gender_idx]}, {age_label}, {expression_labels[expression_idx]}"
            cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image_cv, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            print(f"人脸 {i+1}: 性别={gender_labels[gender_idx]}({gender_conf:.3f}), "
                  f"年龄={age_label}({age_conf:.3f}), "
                  f"表情={expression_labels[expression_idx]}({expression_conf:.3f})")
    else:
        print("未检测到人脸")
    
    # 显示结果图像
    if len(results) > 0:
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title('人脸检测和属性识别结果')
        plt.show()
    
    return results

# 运行主程序
if __name__ == "__main__":
    # 设置路径
    model_path = r"C:\Users\86159\Desktop\swin-small-mlp-20250115-110752-best.pth"
    image_path = r"C:\Users\86159\Desktop\1.jpg"
    
    try:
        results = predict_image_attributes(image_path, model_path)
        
        # 打印汇总结果
        print("\n" + "="*50)
        print("识别结果汇总:")
        print("="*50)
        for result in results:
            print(f"\n人脸 {result['face_id']}:")
            print(f"  位置: {result['box']}")
            print(f"  性别: {result['gender']} (置信度: {result['gender_confidence']:.3f})")
            print(f"  年龄: {result['age']} (置信度: {result['age_confidence']:.3f})")
            print(f"  表情: {result['expression']} (置信度: {result['expression_confidence']:.3f})")
            
    except Exception as e:
        print(f"程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        print("请检查以下可能的问题:")
        print("1. 模型文件路径是否正确")
        print("2. 图片文件是否存在且格式正确")
        print("3. 是否安装了所有必需的库")