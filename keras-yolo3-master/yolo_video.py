# import sys
# import argparse
# from yolo import YOLO, detect_video
# from PIL import Image

# def detect_img(yolo):
#     while True:
#         img = input('Input image filename:')
#         try:
#             image = Image.open(img)
#         except:
#             print('Open Error! Try again!')
#             continue
#         else:
#             r_image = yolo.detect_image(image)
#             r_image.show()
#     yolo.close_session()

# FLAGS = None

# if __name__ == '__main__':
#     # class YOLO defines the default value, so suppress any default here
#     parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
#     '''
#     Command line options
#     '''
#     parser.add_argument(
#         '--model', type=str,
#         help='path to model weight file, default ' + YOLO.get_defaults("model_path")
#     )

#     parser.add_argument(
#         '--anchors', type=str,
#         help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
#     )

#     parser.add_argument(
#         '--classes', type=str,
#         help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
#     )

#     parser.add_argument(
#         '--gpu_num', type=int,
#         help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
#     )

#     parser.add_argument(
#         '--image', default=False, action="store_true",
#         help='Image detection mode, will ignore all positional arguments'
#     )
#     '''
#     Command line positional arguments -- for video detection mode
#     '''
#     parser.add_argument(
#         "--input", nargs='?', type=str,required=False,default='./path2your_video',
#         help = "Video input path"
#     )

#     parser.add_argument(
#         "--output", nargs='?', type=str, default="",
#         help = "[Optional] Video output path"
#     )

#     FLAGS = parser.parse_args()

#     if FLAGS.image:
#         """
#         Image detection mode, disregard any remaining command line arguments
#         """
#         print("Image detection mode")
#         if "input" in FLAGS:
#             print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
#         detect_img(YOLO(**vars(FLAGS)))
#     elif "input" in FLAGS:
#         detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
#     else:
#         print("Must specify at least video_input_path.  See usage with --help.")













import sys
import argparse
import glob
import os
from yolo import YOLO, detect_video
from PIL import Image

def detect_img(yolo, input_dir, output_dir):
    """
    批量检测图片函数
    input_dir: 输入图片文件夹路径
    output_dir: 输出结果文件夹路径
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    # 获取所有jpg图片文件
    # 使用os.path.join确保路径正确，支持不同操作系统
    path_pattern = os.path.join(input_dir, "*.jpg")
    jpg_files = glob.glob(path_pattern)
    
    if not jpg_files:
        print(f"在目录 {input_dir} 中未找到jpg图片文件")
        return
    
    print(f"找到 {len(jpg_files)} 张图片进行检测")
    
    # 批量处理图片
    for i, jpgfile in enumerate(jpg_files):
        try:
            # 打开图片
            img = Image.open(jpgfile)
            print(f"处理图片 {i+1}/{len(jpg_files)}: {os.path.basename(jpgfile)}")
            
            # 进行目标检测
            r_image = yolo.detect_image(img)
            
            # 确保图片为RGB模式（避免RGBA等问题）
            if r_image.mode != 'RGB':
                r_image = r_image.convert('RGB')
            
            # 构建输出路径
            base_name = os.path.basename(jpgfile)
            output_path = os.path.join(output_dir, f"detected_{base_name}")
            
            # 保存结果图片
            r_image.save(output_path, quality=95)
            print(f"结果已保存: {output_path}")
            
        except Exception as e:
            print(f"处理图片 {jpgfile} 时出错: {e}")
            continue
    
    print("批量检测完成!")
    yolo.close_session()

def detect_img_interactive(yolo):
    """保留原有的交互式检测功能（可选）"""
    while True:
        img = input('Input image filename (or "quit" to exit):')
        if img.lower() == 'quit':
            break
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
            
            # 询问是否保存
            save = input('Save this image? (y/n): ')
            if save.lower() == 'y':
                save_path = input('Enter save path: ')
                r_image.save(save_path)
                print(f"Image saved to: {save_path}")
    yolo.close_session()

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    
    # 新增参数：输入图片目录
    parser.add_argument(
        '--input_dir', type=str,
        help='Directory containing images to process'
    )
    
    # 新增参数：输出结果目录
    parser.add_argument(
        '--output_dir', type=str,
        help='Directory to save detection results'
    )
    
    # 新增参数：交互式模式
    parser.add_argument(
        '--interactive', default=False, action="store_true",
        help='Use interactive mode (single image) instead of batch processing'
    )
    
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_video',
        help="Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        print("Image detection mode")
        
        if FLAGS.interactive:
            # 交互式单张图片检测模式
            print("使用交互式模式")
            detect_img_interactive(YOLO(**vars(FLAGS)))
        elif FLAGS.input_dir and FLAGS.output_dir:
            # 批量图片检测模式
            print(f"批量处理模式: 输入目录={FLAGS.input_dir}, 输出目录={FLAGS.output_dir}")
            detect_img(YOLO(**vars(FLAGS)), FLAGS.input_dir, FLAGS.output_dir)
        else:
            print("错误: 批量处理需要指定 --input_dir 和 --output_dir 参数")
            print("或者使用 --interactive 进行交互式检测")
            print("使用示例:")
            print("python yolo_video.py --image --input_dir F:\\data\\VOC2007\\test --output_dir F:\\data\\VOC2007\\results")
            print("python yolo_video.py --image --interactive")
    elif "input" in FLAGS:
        # 视频检测模式
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path. See usage with --help.")