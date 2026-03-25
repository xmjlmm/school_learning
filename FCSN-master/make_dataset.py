# from torchvision import transforms, models
# import torch
# from torch import nn
# from PIL import Image
# from pathlib import Path
# import cv2
# import h5py
# import numpy as np
# from tqdm import tqdm
# import argparse
# import pdb


# parser = argparse.ArgumentParser()
# parser.add_argument('--video_dir', type=str, help='directory containing mp4 file of specified dataset.', default='F:/data/ydata-tvsum50-v1_1/video')
# parser.add_argument('--h5_path', type=str, help='save path of the generated dataset, which should be a hdf5 file.', default='F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5')
# parser.add_argument('--vsumm_data', type=str, help='preprocessed dataset path from this repo: https://github.com/KaiyangZhou/pytorch-vsumm-reinforce, which should be a hdf5 file. We copy cps and some other info from it.', default='F:/data/ydata-tvsum50-v1_1/eccv16_dataset_tvsum_google_pool5.h5')


# # parser.add_argument('--video_dir', type=str, help='directory containing mp4 file of specified dataset.', default='../data/TVSum_video')
# # parser.add_argument('--h5_path', type=str, help='save path of the generated dataset, which should be a hdf5 file.', default='../data/fcsn_tvsum.h5')
# # parser.add_argument('--vsumm_data', type=str, help='preprocessed dataset path from this repo: https://github.com/KaiyangZhou/pytorch-vsumm-reinforce, which should be a hdf5 file. We copy cps and some other info from it.', default='../data/eccv_datasets/eccv16_dataset_tvsum_google_pool5.h5')

# args = parser.parse_args()
# video_dir = args.video_dir
# h5_path = args.h5_path
# vsumm_data = h5py.File(args.vsumm_data)


# class Rescale(object):
#     """Rescale a image to a given size.

#     Args:
#         output_size (tuple or int): Desired output size. If tuple, output is matched to output_size. If int, smaller of image edges is matched to output_size keeping aspect ratio the same.
#     """

#     def __init__(self, *output_size):
#         self.output_size = output_size

#     def __call__(self, image):
#         """
#         Args:
#             image (PIL.Image) : PIL.Image object to rescale
#         """
#         new_h, new_w = self.output_size
#         new_h, new_w = int(new_h), int(new_w)
#         img = image.resize((new_w, new_h), resample=Image.BILINEAR)
#         return img


# transform = transforms.Compose([
#     Rescale(224, 224),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])


# net = models.googlenet(pretrained=True).float().cuda()
# net.eval()
# fea_net = nn.Sequential(*list(net.children())[:-2])


# def sum_fscore(overlap_arr, true_sum_arr, oracle_sum):
#     fscores = []
#     for overlap, true_sum in zip(overlap_arr, true_sum_arr):
#         precision = overlap / (oracle_sum + 1e-8);
#         recall = overlap / (true_sum + 1e-8);
#         if precision == 0 and recall == 0:
#             fscore = 0
#         else:
#             fscore = 2 * precision * recall / (precision + recall)
#         fscores.append(fscore)
#     return sum(fscores) / len(fscores)


# def get_oracle_summary(user_summary):
#     n_user, n_frame = user_summary.shape
#     oracle_summary = np.zeros(n_frame)
#     overlap_arr = np.zeros(n_user)
#     oracle_sum = 0
#     true_sum_arr = user_summary.sum(axis=1)
#     priority_idx = np.argsort(-user_summary.sum(axis=0))
#     best_fscore = 0
#     for idx in priority_idx:
#         oracle_sum += 1
#         for usr_i in range(n_user):
#             overlap_arr[usr_i] += user_summary[usr_i][idx]
#         cur_fscore = sum_fscore(overlap_arr, true_sum_arr, oracle_sum)
#         if cur_fscore > best_fscore:
#             best_fscore = cur_fscore
#             oracle_summary[idx] = 1
#         else:
#             break
#     tqdm.write('Overlap: '+str(overlap_arr))
#     tqdm.write('True summary n_key: '+str(true_sum_arr))
#     tqdm.write('Oracle smmary n_key: '+str(oracle_sum))
#     tqdm.write('Final F-score: '+str(best_fscore))
#     return oracle_summary


# def video2fea(video_path, h5_f):
#     video = cv2.VideoCapture(video_path.as_uri())
#     idx = video_path.as_uri().split('.')[0].split('/')[-1]
#     tqdm.write('Processing video '+idx)
#     length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
#     ratio = length//320
#     fea = []
#     label = []
#     usr_sum_arr = vsumm_data['video_'+idx]['user_summary'][()]
#     usr_sum = get_oracle_summary(usr_sum_arr) 
#     cps = vsumm_data['video_'+idx]['change_points'][()]
#     n_frame_per_seg = vsumm_data['video_'+idx]['n_frame_per_seg'][()]
#     i = 0
#     success, frame = video.read()
#     while success:
#         if (i+1) % ratio == 0:
#             fea.append(fea_net(transform(Image.fromarray(frame)).cuda().unsqueeze(0)).squeeze().detach().cpu())
#             try:
#                 label.append(usr_sum[i])
#             except:
#                 pdb.set_trace()
#         i += 1
#         success, frame = video.read()
#     fea = torch.stack(fea)
#     fea = fea[:320]
#     label = label[:320]
#     v_data = h5_f.create_group('video_'+idx)
#     v_data['feature'] = fea.numpy()
#     v_data['label'] = label
#     v_data['length'] = len(usr_sum)
#     v_data['change_points'] = cps
#     v_data['n_frame_per_seg'] = n_frame_per_seg
#     v_data['picks'] = [ratio*i for i in range(320)]
#     v_data['user_summary'] = usr_sum_arr
#     if fea.shape[0] != 320 or len(label) != 320:
#         print('error in video ', idx, feashape[0], len(label))


# def make_dataset(video_dir, h5_path):
#     video_dir = Path(video_dir).resolve()
#     video_list = list(video_dir.glob('*.mp4'))
#     video_list.sort()
#     with h5py.File(h5_path, 'w') as h5_f:
#         for video_path in tqdm(video_list, desc='Video', ncols=80, leave=False):
#             video2fea(video_path, h5_f)
    
    
# if __name__ == '__main__':
#     make_dataset(video_dir, h5_path)


# vsumm_data.close()




from torchvision import transforms, models
import torch
from torch import nn
from PIL import Image
from pathlib import Path
import cv2
import h5py
import numpy as np
from tqdm import tqdm
import argparse
import pdb
import warnings

# 忽略torchvision的弃用警告
warnings.filterwarnings("ignore", category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--video_dir', type=str, help='directory containing mp4 file of specified dataset.', default='F:/data/ydata-tvsum50-v1_1/video')
parser.add_argument('--h5_path', type=str, help='save path of the generated dataset, which should be a hdf5 file.', default='F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5')
parser.add_argument('--vsumm_data', type=str, help='preprocessed dataset path from this repo: https://github.com/KaiyangZhou/pytorch-vsumm-reinforce, which should be a hdf5 file. We copy cps and some other info from it.', default='F:/data/ydata-tvsum50-v1_1/eccv16_dataset_tvsum_google_pool5.h5')

args = parser.parse_args()
video_dir = args.video_dir
h5_path = args.h5_path
vsumm_data = h5py.File(args.vsumm_data, 'r')  # 以只读模式打开参考HDF5文件


class Rescale(object):
    """Rescale a image to a given size.

    Args:
        output_size (tuple or int): Desired output size. If tuple, output is matched to output_size. If int, smaller of image edges is matched to output_size keeping aspect ratio the same.
    """

    def __init__(self, *output_size):
        self.output_size = output_size

    def __call__(self, image):
        """
        Args:
            image (PIL.Image) : PIL.Image object to rescale
        """
        new_h, new_w = self.output_size
        new_h, new_w = int(new_h), int(new_w)
        img = image.resize((new_w, new_h), resample=Image.BILINEAR)
        return img


transform = transforms.Compose([
    Rescale(224, 224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# 使用新的weights参数替代已弃用的pretrained参数
net = models.googlenet(weights=models.GoogLeNet_Weights.IMAGENET1K_V1).float().cuda()
net.eval()
fea_net = nn.Sequential(*list(net.children())[:-2])


def sum_fscore(overlap_arr, true_sum_arr, oracle_sum):
    """计算F-score"""
    fscores = []
    for overlap, true_sum in zip(overlap_arr, true_sum_arr):
        precision = overlap / (oracle_sum + 1e-8)
        recall = overlap / (true_sum + 1e-8)
        if precision == 0 and recall == 0:
            fscore = 0
        else:
            fscore = 2 * precision * recall / (precision + recall)
        fscores.append(fscore)
    return sum(fscores) / len(fscores)


def get_oracle_summary(user_summary):
    """生成oracle摘要"""
    n_user, n_frame = user_summary.shape
    oracle_summary = np.zeros(n_frame)
    overlap_arr = np.zeros(n_user)
    oracle_sum = 0
    true_sum_arr = user_summary.sum(axis=1)
    priority_idx = np.argsort(-user_summary.sum(axis=0))
    best_fscore = 0
    for idx in priority_idx:
        oracle_sum += 1
        for usr_i in range(n_user):
            overlap_arr[usr_i] += user_summary[usr_i][idx]
        cur_fscore = sum_fscore(overlap_arr, true_sum_arr, oracle_sum)
        if cur_fscore > best_fscore:
            best_fscore = cur_fscore
            oracle_summary[idx] = 1
        else:
            break
    tqdm.write('Overlap: ' + str(overlap_arr))
    tqdm.write('True summary n_key: ' + str(true_sum_arr))
    tqdm.write('Oracle summary n_key: ' + str(oracle_sum))
    tqdm.write('Final F-score: ' + str(best_fscore))
    return oracle_summary


def video2fea(video_path, h5_f, video_index):
    """
    处理单个视频并提取特征
    
    Args:
        video_path: 视频文件路径
        h5_f: 输出的HDF5文件对象
        video_index: 视频的索引（从1开始），用于匹配HDF5中的键名
    """
    try:
        # 使用更稳定的视频读取方式
        video = cv2.VideoCapture(str(video_path))
        idx = str(video_index)  # 使用传入的索引作为ID
        
        tqdm.write(f'Processing video {video_path.name} with index {idx}')
        
        # 检查该ID在HDF5中是否存在
        video_key = f'video_{idx}'
        if video_key not in vsumm_data:
            print(f"Warning: {video_key} not found in reference HDF5, skipping video {video_path.name}")
            return
        
        # 获取视频基本信息
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        ratio = max(length // 320, 1)  # 确保ratio至少为1
        
        tqdm.write(f'Video length: {length} frames, FPS: {fps:.2f}, Ratio: {ratio}')
        
        fea = []
        label = []
        
        # 从参考HDF5文件中获取数据
        usr_sum_arr = vsumm_data[video_key]['user_summary'][()]
        usr_sum = get_oracle_summary(usr_sum_arr) 
        cps = vsumm_data[video_key]['change_points'][()]
        n_frame_per_seg = vsumm_data[video_key]['n_frame_per_seg'][()]
        
        i = 0
        frames_processed = 0
        success, frame = video.read()
        
        # 处理视频帧
        while success and frames_processed < 320:
            if (i + 1) % ratio == 0:
                # 转换BGR到RGB并处理帧
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                
                # 提取特征
                with torch.no_grad():
                    input_tensor = transform(pil_image).unsqueeze(0).cuda()
                    frame_fea = fea_net(input_tensor).squeeze().detach().cpu()
                
                fea.append(frame_fea)
                
                # 确保不越界地获取标签
                if i < len(usr_sum):
                    label.append(usr_sum[i])
                else:
                    # 如果视频比标注长，用0填充
                    label.append(0)
                
                frames_processed += 1
                if frames_processed >= 320:
                    break
            
            i += 1
            success, frame = video.read()
        
        # 确保特征数量为320
        if len(fea) < 320:
            # 如果帧数不足，用零填充
            padding_count = 320 - len(fea)
            last_fea = fea[-1] if fea else torch.zeros(1024)  # GoogLeNet特征维度是1024
            last_label = label[-1] if label else 0
            
            # 填充特征和标签
            for _ in range(padding_count):
                fea.append(last_fea.clone())
                label.append(last_label)
            
            tqdm.write(f'Padded {padding_count} frames to reach 320')
        
        # 转换为张量
        fea_tensor = torch.stack(fea[:320])
        label = label[:320]
        
        # 创建视频数据组
        v_data = h5_f.create_group(f'video_{idx}')
        v_data['feature'] = fea_tensor.numpy()
        v_data['label'] = label
        v_data['length'] = len(usr_sum)
        v_data['change_points'] = cps
        v_data['n_frame_per_seg'] = n_frame_per_seg
        v_data['picks'] = [ratio * i for i in range(min(320, len(fea)))]
        v_data['user_summary'] = usr_sum_arr
        
        tqdm.write(f'Successfully processed video {idx}, features shape: {fea_tensor.shape}')
        
    except Exception as e:
        print(f"Error processing video {video_path.name}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'video' in locals():
            video.release()


def make_dataset(video_dir, h5_path):
    """
    创建数据集
    
    Args:
        video_dir: 视频文件目录
        h5_path: 输出的HDF5文件路径
    """
    video_dir = Path(video_dir).resolve()
    video_list = list(video_dir.glob('*.mp4'))
    video_list.sort()  # 按文件名排序，确保顺序一致 [6](@ref)
    
    print(f"Found {len(video_list)} video files")
    print(f"HDF5 reference file has {len(vsumm_data.keys())} video groups")
    
    # 显示映射关系
    print("\nMapping relationship (first 10 files):")
    for i, video_path in enumerate(video_list[:10]):
        video_key = f'video_{i+1}'
        exists_in_ref = video_key in vsumm_data
        status = "✓" if exists_in_ref else "✗"
        print(f"{status} {video_path.name} -> {video_key}")
    
    # 检查数量是否匹配
    if len(video_list) != len([k for k in vsumm_data.keys() if k.startswith('video_')]):
        print(f"Warning: Video file count ({len(video_list)}) doesn't match HDF5 key count")
    
    # 创建输出HDF5文件
    with h5py.File(h5_path, 'w') as h5_f:
        for i, video_path in enumerate(tqdm(video_list, desc='Processing Videos', ncols=80)):
            video_index = i + 1  # 索引从1开始，匹配HDF5中的video_1, video_2等
            
            # 检查HDF5中是否存在对应的键
            video_key = f'video_{video_index}'
            if video_key not in vsumm_data:
                print(f"Skipping video {video_path.name} - {video_key} not found in reference HDF5")
                continue
                
            video2fea(video_path, h5_f, video_index)
    
    print(f"Dataset creation completed. Output saved to: {h5_path}")


if __name__ == '__main__':
    try:
        make_dataset(video_dir, h5_path)
    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        vsumm_data.close()
