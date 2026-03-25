# import json
# import csv
# import h5py
# import cv2
# import os
# import argparse
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns


# parser = argparse.ArgumentParser(description='Generate keyshots, keyframes and score bar.')
# parser.add_argument('--h5_path', type=str, help='path to hdf5 file that contains information of a dataset.', default=r'F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5')
# parser.add_argument('-j', '--json_path', type=str, help='path to json file that stores pred score output by model, it should be saved in score_dir.', default=r'F:/data/ydata-tvsum50-v1_1/score_dir/epoch-499.json')
# parser.add_argument('-r', '--data_root', type=str, help='path to directory of original dataset.', default=r'F:\data')
# parser.add_argument('-s', '--save_dir', type=str, help='path to directory where generating results should be saved.', default=r'F:/data/ydata-tvsum50-v1_1/Results')
# parser.add_argument('-b', '--bar', action='store_true', help='whether to plot score bar.')

# args = parser.parse_args()
# h5_path = args.h5_path
# json_path = args.json_path
# data_root = args.data_root
# save_dir = args.save_dir
# bar = args.bar
# video_dir = os.path.join(data_root, 'ydata-tvsum50-v1_1', 'video')
# anno_path = os.path.join(data_root, 'ydata-tvsum50-v1_1', 'data', 'ydata-tvsum50-anno.tsv')
# f_data = h5py.File(h5_path)
# with open(json_path) as f:
#     json_dict = json.load(f)
#     ids = json_dict.keys()


# def get_keys(id):
#     video_info = f_data['video_' + id]
#     video_path = os.path.join(video_dir, id+'.mp4')
#     cps = video_info['change_points'][()]
#     pred_score = json_dict[id]['pred_score']
#     pred_selected = json_dict[id]['pred_selected']

#     video = cv2.VideoCapture(video_path)
#     frames = []
#     success, frame = video.read()
#     while success:
#         frames.append(frame)
#         success, frame = video.read()
#     frames = np.array(frames)
#     keyshots = []
#     for sel in pred_selected:
#         for i in range(cps[sel][0], cps[sel][1]):
#             keyshots.append(frames[i])
#     keyshots = np.array(keyshots)

#     write_path = os.path.join(save_dir, id, 'summary.avi')
#     video_writer = cv2.VideoWriter(write_path, cv2.VideoWriter_fourcc(*'XVID'), 24, keyshots.shape[2:0:-1])
#     for frame in keyshots:
#         video_writer.write(frame)
#     video_writer.release()

#     keyframe_idx = [np.argmax(pred_score[cps[sel][0] : cps[sel][1]]) + cps[sel][0] for sel in pred_selected]
#     keyframes = frames[keyframe_idx]

#     keyframe_dir = os.path.join(save_dir, id, 'keyframes')
#     os.mkdir(keyframe_dir)
#     for i, img in enumerate(keyframes):
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         plt.axis('off')
#         plt.imshow(img)
#         plt.savefig(os.path.join(keyframe_dir, '{}.jpg'.format(i)))


# def plot_bar():
#     with open(anno_path) as f:
#         csv_reader = csv.reader(f, delimiter='\t')
#         csv_dict = {}
#         idx = 0
#         for row in csv_reader:
#             score = np.array([int(i) for i in row[2].split(',')])
#             if str(idx//20+1) in ids:
#                 if idx % 20 == 0:
#                     csv_dict[str(idx//20+1)] = score/20
#                 else:
#                     csv_dict[str(idx//20+1)] += score/20
#             idx += 1
    
#     sns.set()
#     fig, ax = plt.subplots(ncols=1, nrows=len(ids), figsize=(30, 20))
#     fig.tight_layout()
#     for id, axi in zip(ids, ax.flat):
#             scores = csv_dict[id]
#             pred_summary = json_dict[id]['pred_summary']
#             axi.bar(left=list(range(len(scores))), height=scores, color=['lightseagreen' if i == 0
#                 else 'orange' for i in pred_summary], edgecolor=None)
#             axi.set_title(id)
#     save_path = os.path.join(save_dir, 'result-bar.png')
#     plt.savefig(save_path)


# def gen_summary():
#     if not os.path.exists(save_dir):
#         os.mkdir(save_dir)

#     for id in ids:
#         os.mkdir(os.path.join(save_dir, id))
#         get_keys(id)
    
#     if bar:
#         plot_bar()


# if __name__ == '__main__':
#     plt.switch_backend('agg')
#     gen_summary()


# f_data.close()




# import json
# import csv
# import h5py
# import cv2
# import os
# import argparse
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# parser = argparse.ArgumentParser(description='Generate keyshots, keyframes and score bar.')
# parser.add_argument('--h5_path', type=str, help='path to hdf5 file that contains information of a dataset.', default='F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5')
# parser.add_argument('-j', '--json_path', type=str, help='path to json file that stores pred score output by model, it should be saved in score_dir.', default='F:/data/ydata-tvsum50-v1_1/score_dir/epoch-499.json')
# parser.add_argument('-r', '--data_root', type=str, help='path to directory of original dataset.', default='F:/data')
# parser.add_argument('-s', '--save_dir', type=str, help='path to directory where generating results should be saved.', default='F:/data/ydata-tvsum50-v1_1/Results')
# parser.add_argument('-b', '--bar', action='store_true', help='whether to plot score bar.')

# args = parser.parse_args()
# h5_path = args.h5_path
# json_path = args.json_path
# data_root = args.data_root
# save_dir = args.save_dir
# bar = args.bar
# video_dir = "F:/data/ydata-tvsum50-v1_1/video"
# anno_path = "F:/data/ydata-tvsum50-v1_1/ydata-tvsum50-data/data/ydata-tvsum50-anno.tsv"

# def get_keys(id, video_path, f_data, json_dict):
#     """处理单个视频并生成关键片段和关键帧"""
#     try:
#         # 检查HDF5中是否存在该视频
#         video_key = 'video_' + id
#         if video_key not in f_data:
#             print(f"错误: 在HDF5文件中未找到视频 {video_key}")
#             return False
        
#         video_info = f_data[video_key]
        
#         # 检查视频文件是否存在
#         if not os.path.exists(video_path):
#             print(f"错误: 视频文件不存在: {video_path}")
#             return False
        
#         cps = video_info['change_points'][()]
#         pred_score = json_dict[id]['pred_score']
#         pred_selected = json_dict[id]['pred_selected']

#         # 打开视频文件并检查是否成功
#         video = cv2.VideoCapture(video_path)
#         if not video.isOpened():
#             print(f"错误: 无法打开视频文件: {video_path}")
#             return False
        
#         # 读取所有帧
#         frames = []
#         success, frame = video.read()
#         frame_count = 0
        
#         while success and frame_count < 10000:  # 安全限制，防止无限循环
#             frames.append(frame)
#             success, frame = video.read()
#             frame_count += 1
        
#         video.release()
        
#         # 检查是否成功读取帧
#         if len(frames) == 0:
#             print(f"错误: 视频 {id} 没有读取到任何帧")
#             return False
        
#         frames = np.array(frames)
#         print(f"视频 {id} 成功读取 {len(frames)} 帧")
        
#         # 生成关键片段 - 添加安全检查
#         keyshots = []
#         valid_segments = 0
        
#         for sel in pred_selected:
#             # 确保索引在有效范围内
#             if sel < len(cps):
#                 start, end = cps[sel]
#                 # 确保不超出帧数组范围
#                 start = max(0, min(start, len(frames)-1))
#                 end = max(0, min(end, len(frames)-1))
                
#                 if start <= end:  # 确保有效的范围
#                     for i in range(start, end + 1):
#                         if i < len(frames):  # 额外安全检查
#                             keyshots.append(frames[i])
#                     valid_segments += 1
        
#         if len(keyshots) == 0:
#             print(f"警告: 视频 {id} 没有生成任何关键片段")
#             # 不视为错误，但跳过视频写入
#             return True
        
#         keyshots = np.array(keyshots)
        
#         # 创建保存目录
#         video_save_dir = os.path.join(save_dir, id)
#         os.makedirs(video_save_dir, exist_ok=True)
        
#         # 写入关键片段视频
#         write_path = os.path.join(video_save_dir, 'summary.avi')
#         if len(keyshots) > 0:
#             # 获取帧的尺寸
#             frame_height, frame_width = keyshots[0].shape[:2]
#             video_writer = cv2.VideoWriter(write_path, cv2.VideoWriter_fourcc(*'XVID'), 24, 
#                                          (frame_width, frame_height))
            
#             for frame in keyshots:
#                 video_writer.write(frame)
#             video_writer.release()
#             print(f"已生成关键片段视频: {write_path}")
        
#         # 生成关键帧 - 添加安全检查
#         keyframe_idx = []
#         for sel in pred_selected:
#             if sel < len(cps):  # 确保索引有效
#                 start, end = cps[sel]
#                 # 确保不越界
#                 start = max(0, min(start, len(frames)-1))
#                 end = max(0, min(end, len(frames)-1))
                
#                 if start <= end and end < len(pred_score) and start < len(pred_score):
#                     # 在变更点范围内找到预测分数最高的帧
#                     segment_scores = pred_score[start:end+1]
#                     if len(segment_scores) > 0:
#                         local_max_idx = np.argmax(segment_scores)
#                         absolute_idx = start + local_max_idx
#                         if absolute_idx < len(frames):  # 最终检查
#                             keyframe_idx.append(absolute_idx)
        
#         keyframes = []
#         for idx in keyframe_idx:
#             if idx < len(frames):
#                 keyframes.append(frames[idx])
        
#         if len(keyframes) > 0:
#             keyframe_dir = os.path.join(video_save_dir, 'keyframes')
#             os.makedirs(keyframe_dir, exist_ok=True)
            
#             for i, img in enumerate(keyframes):
#                 img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                 plt.figure(figsize=(8, 6))
#                 plt.axis('off')
#                 plt.imshow(img_rgb)
#                 plt.savefig(os.path.join(keyframe_dir, f'{i}.jpg'), bbox_inches='tight', pad_inches=0)
#                 plt.close()
#             print(f"已生成 {len(keyframes)} 个关键帧")
#         else:
#             print(f"警告: 视频 {id} 没有生成关键帧")
        
#         return True
        
#     except Exception as e:
#         print(f"处理视频 {id} 时发生错误: {e}")
#         import traceback
#         traceback.print_exc()
#         return False

# def plot_bar(json_dict, ids):
#     """绘制分数条形图 - 根据图片描述优化样式"""
#     try:
#         print(f"开始生成条形图，注解文件路径: {anno_path}")
        
#         # 检查注解文件是否存在
#         if not os.path.exists(anno_path):
#             print(f"错误: 注解文件不存在: {anno_path}")
#             return
        
#         # 读取注解文件
#         csv_dict = {}
#         idx = 0
#         valid_rows = 0
        
#         with open(anno_path, 'r', encoding='utf-8') as f:
#             csv_reader = csv.reader(f, delimiter='\t')
            
#             for row_num, row in enumerate(csv_reader):
#                 if len(row) < 3:
#                     continue
                
#                 try:
#                     # 解析分数数据
#                     score_values = [int(i) for i in row[2].split(',')]
#                     video_id = str(idx // 20 + 1)  # 每20行对应一个视频
                    
#                     if video_id in ids:
#                         if idx % 20 == 0:
#                             csv_dict[video_id] = np.array(score_values) / 20.0
#                         else:
#                             if video_id in csv_dict:
#                                 csv_dict[video_id] += np.array(score_values) / 20.0
#                             else:
#                                 csv_dict[video_id] = np.array(score_values) / 20.0
                        
#                         valid_rows += 1
                    
#                     idx += 1
                    
#                 except (ValueError, IndexError) as e:
#                     print(f"警告: 解析第{row_num}行时出错: {e}")
#                     continue
        
#         print(f"成功处理 {valid_rows} 行注解数据")
#         print(f"有效的视频ID: {list(csv_dict.keys())}")
        
#         if not csv_dict:
#             print("错误: 没有有效的注解数据")
#             return
        
#         # 设置样式 - 根据图片描述调整
#         sns.set_style("whitegrid")  # 白色网格背景
#         plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']  # 支持中文显示
#         plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
        
#         # 根据视频数量调整布局
#         n_videos = len(ids)
#         ncols = min(3, n_videos)  # 每行最多3个子图
#         nrows = (n_videos + ncols - 1) // ncols  # 计算需要的行数
        
#         # 创建图形 - 根据图片描述调整尺寸
#         fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols, 4*nrows))
#         fig.suptitle('视频关键帧得分分布图', fontsize=16, fontweight='bold')
        
#         # 如果只有一个子图，确保axes是数组形式
#         if n_videos == 1:
#             axes = np.array([axes])
#         if axes.ndim == 1:
#             axes = axes.reshape(1, -1)
        
#         # 为每个视频创建子图
#         for i, video_id in enumerate(ids):
#             row = i // ncols
#             col = i % ncols
            
#             if video_id in csv_dict:
#                 scores = csv_dict[video_id]
                
#                 # 获取预测摘要信息
#                 pred_summary = json_dict.get(video_id, {}).get('pred_summary', [])
                
#                 # 确保pred_summary长度与scores匹配
#                 if len(pred_summary) != len(scores):
#                     min_len = min(len(pred_summary), len(scores))
#                     if min_len == 0:
#                         print(f"警告: 视频 {video_id} 的pred_summary或scores为空")
#                         continue
#                     pred_summary = pred_summary[:min_len]
#                     scores = scores[:min_len]
                
#                 # 创建颜色数组 - 使用图片描述中的蓝绿色和橙色
#                 colors = ['lightseagreen' if flag == 0 else 'orange' for flag in pred_summary]
                
#                 # 绘制条形图 - 根据图片描述调整样式
#                 x_positions = np.arange(len(scores))
#                 axes[row, col].bar(x_positions, scores, color=colors, 
#                                   edgecolor='gray', linewidth=0.5, alpha=0.8)
                
#                 # 设置图表属性
#                 axes[row, col].set_title(f'视频 {video_id}', fontsize=12, fontweight='bold')
#                 axes[row, col].set_xlabel('帧索引')
#                 axes[row, col].set_ylabel('得分')
                
#                 # 设置网格样式 - 浅灰色网格
#                 axes[row, col].grid(True, alpha=0.3, color='lightgray')
                
#                 # 添加图例（只在第一个子图添加）
#                 if i == 0:
#                     from matplotlib.patches import Patch
#                     legend_elements = [
#                         Patch(facecolor='orange', label='关键帧'),
#                         Patch(facecolor='lightseagreen', label='非关键帧')
#                     ]
#                     axes[row, col].legend(handles=legend_elements, loc='upper right')
#             else:
#                 axes[row, col].text(0.5, 0.5, f'视频 {video_id}\n无数据', 
#                                    ha='center', va='center', transform=axes[row, col].transAxes)
#                 axes[row, col].set_title(f'视频 {video_id}')
        
#         # 隐藏多余的子图
#         for i in range(n_videos, nrows * ncols):
#             row = i // ncols
#             col = i % ncols
#             axes[row, col].set_visible(False)
        
#         plt.tight_layout()
#         plt.subplots_adjust(top=0.95)  # 为总标题留出空间
        
#         # 保存图片
#         save_path = os.path.join(save_dir, 'result-bar.png')
#         plt.savefig(save_path, dpi=300, bbox_inches='tight')
#         plt.close()
        
#         print(f"✓ 条形图已保存: {save_path}")
#         print(f"✓ 包含 {len([vid for vid in ids if vid in csv_dict])}/{len(ids)} 个视频的数据")
        
#     except Exception as e:
#         print(f"生成条形图时发生错误: {e}")
#         import traceback
#         traceback.print_exc()

# def gen_summary():
#     """生成摘要"""
#     try:
#         # 加载HDF5文件
#         f_data = h5py.File(h5_path, 'r')
        
#         # 加载JSON预测结果
#         with open(json_path) as f:
#             json_dict = json.load(f)
#             ids = list(json_dict.keys())
        
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)
        
#         # 获取视频文件列表并排序
#         video_files = sorted([f for f in os.listdir(video_dir) if f.endswith('.mp4')])
#         print(f"找到 {len(video_files)} 个视频文件")
#         print(f"JSON中有 {len(ids)} 个视频ID需要处理")
        
#         # 显示前几个文件的映射关系
#         print("\n视频文件与ID的映射关系 (前10个):")
#         for i, video_file in enumerate(video_files[:10]):
#             video_id = str(i + 1)
#             if video_id in ids:
#                 status = "✓"
#             else:
#                 status = "✗"
#             print(f"{status} {video_file} -> video_{video_id}")
        
#         success_count = 0
#         total_count = len(ids)
        
#         print(f"\n开始处理 {total_count} 个视频...")
        
#         for id in ids:
#             print(f"\n处理视频 {id}...")
            
#             try:
#                 # 将ID转换为整数索引
#                 id_int = int(id)
#                 if id_int < 1 or id_int > len(video_files):
#                     print(f"错误: ID {id} 超出范围 (1-{len(video_files)})")
#                     continue
                
#                 # 获取对应的视频文件名（索引从0开始）
#                 video_filename = video_files[id_int - 1]
#                 video_path = os.path.join(video_dir, video_filename)
                
#                 print(f"映射: video_{id} -> {video_filename}")
                
#                 if get_keys(id, video_path, f_data, json_dict):
#                     success_count += 1
#                     print(f"视频 {id} 处理成功")
#                 else:
#                     print(f"视频 {id} 处理失败")
                    
#             except ValueError:
#                 print(f"错误: ID {id} 不是有效的数字")
#             except Exception as e:
#                 print(f"处理视频 {id} 时发生未知错误: {e}")
        
#         print(f"\n处理完成: {success_count}/{total_count} 个视频成功处理")
        
#         # 无论bar参数如何，总是尝试生成条形图
#         if success_count > 0:
#             print("生成分数条形图...")
#             plot_bar(json_dict, ids)
#         else:
#             print("没有成功处理的视频，跳过条形图生成")
        
#         f_data.close()
        
#     except Exception as e:
#         print(f"程序执行错误: {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == '__main__':
#     plt.switch_backend('agg')
#     gen_summary()



import json
import csv
import h5py
import cv2
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Generate keyshots, keyframes and score bar.')
parser.add_argument('--h5_path', type=str, help='path to hdf5 file that contains information of a dataset.', default='F:/data/ydata-tvsum50-v1_1/fcsn_tvsum.h5')
parser.add_argument('-j', '--json_path', type=str, help='path to json file that stores pred score output by model, it should be saved in score_dir.', default='F:/data/ydata-tvsum50-v1_1/score_dir/epoch-49.json')
parser.add_argument('-r', '--data_root', type=str, help='path to directory of original dataset.', default='F:/data')
parser.add_argument('-s', '--save_dir', type=str, help='path to directory where generating results should be saved.', default='F:/data/ydata-tvsum50-v1_1/Results')
parser.add_argument('-b', '--bar', action='store_true', help='whether to plot score bar.')

args = parser.parse_args()
h5_path = args.h5_path
json_path = args.json_path
data_root = args.data_root
save_dir = args.save_dir
bar = args.bar
video_dir = "F:/data/ydata-tvsum50-v1_1/video"
anno_path = "F:/data/ydata-tvsum50-v1_1/ydata-tvsum50-data/data/ydata-tvsum50-anno.tsv"

def get_keys(id, video_path, f_data, json_dict):
    """处理单个视频并生成关键片段和关键帧"""
    try:
        # 检查HDF5中是否存在该视频
        video_key = 'video_' + id
        if video_key not in f_data:
            print(f"错误: 在HDF5文件中未找到视频 {video_key}")
            return False
        
        video_info = f_data[video_key]
        
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"错误: 视频文件不存在: {video_path}")
            return False
        
        cps = video_info['change_points'][()]
        pred_score = json_dict[id]['pred_score']
        pred_selected = json_dict[id]['pred_selected']

        # 打开视频文件并检查是否成功
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print(f"错误: 无法打开视频文件: {video_path}")
            return False
        
        # 读取所有帧
        frames = []
        success, frame = video.read()
        frame_count = 0
        
        while success and frame_count < 10000:  # 安全限制，防止无限循环
            frames.append(frame)
            success, frame = video.read()
            frame_count += 1
        
        video.release()
        
        # 检查是否成功读取帧
        if len(frames) == 0:
            print(f"错误: 视频 {id} 没有读取到任何帧")
            return False
        
        frames = np.array(frames)
        print(f"视频 {id} 成功读取 {len(frames)} 帧")
        
        # 生成关键片段 - 添加安全检查
        keyshots = []
        valid_segments = 0
        
        for sel in pred_selected:
            # 确保索引在有效范围内
            if sel < len(cps):
                start, end = cps[sel]
                # 确保不超出帧数组范围
                start = max(0, min(start, len(frames)-1))
                end = max(0, min(end, len(frames)-1))
                
                if start <= end:  # 确保有效的范围
                    for i in range(start, end + 1):
                        if i < len(frames):  # 额外安全检查
                            keyshots.append(frames[i])
                    valid_segments += 1
        
        if len(keyshots) == 0:
            print(f"警告: 视频 {id} 没有生成任何关键片段")
            # 不视为错误，但跳过视频写入
            return True
        
        keyshots = np.array(keyshots)
        
        # 创建保存目录
        video_save_dir = os.path.join(save_dir, id)
        os.makedirs(video_save_dir, exist_ok=True)
        
        # 写入关键片段视频
        write_path = os.path.join(video_save_dir, 'summary.avi')
        if len(keyshots) > 0:
            # 获取帧的尺寸
            frame_height, frame_width = keyshots[0].shape[:2]
            video_writer = cv2.VideoWriter(write_path, cv2.VideoWriter_fourcc(*'XVID'), 24, 
                                         (frame_width, frame_height))
            
            for frame in keyshots:
                video_writer.write(frame)
            video_writer.release()
            print(f"已生成关键片段视频: {write_path}")
        
        # 生成关键帧 - 添加安全检查
        keyframe_idx = []
        for sel in pred_selected:
            if sel < len(cps):  # 确保索引有效
                start, end = cps[sel]
                # 确保不越界
                start = max(0, min(start, len(frames)-1))
                end = max(0, min(end, len(frames)-1))
                
                if start <= end and end < len(pred_score) and start < len(pred_score):
                    # 在变更点范围内找到预测分数最高的帧
                    segment_scores = pred_score[start:end+1]
                    if len(segment_scores) > 0:
                        local_max_idx = np.argmax(segment_scores)
                        absolute_idx = start + local_max_idx
                        if absolute_idx < len(frames):  # 最终检查
                            keyframe_idx.append(absolute_idx)
        
        keyframes = []
        for idx in keyframe_idx:
            if idx < len(frames):
                keyframes.append(frames[idx])
        
        if len(keyframes) > 0:
            keyframe_dir = os.path.join(video_save_dir, 'keyframes')
            os.makedirs(keyframe_dir, exist_ok=True)
            
            for i, img in enumerate(keyframes):
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                plt.figure(figsize=(8, 6))
                plt.axis('off')
                plt.imshow(img_rgb)
                plt.savefig(os.path.join(keyframe_dir, f'{i}.jpg'), bbox_inches='tight', pad_inches=0)
                plt.close()
            print(f"已生成 {len(keyframes)} 个关键帧")
        else:
            print(f"警告: 视频 {id} 没有生成关键帧")
        
        return True
        
    except Exception as e:
        print(f"处理视频 {id} 时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def plot_bar(json_dict, ids, f_data):
    """绘制分数条形图 - 修复关键帧显示问题"""
    try:
        print(f"开始生成条形图，注解文件路径: {anno_path}")
        
        # 检查注解文件是否存在
        if not os.path.exists(anno_path):
            print(f"错误: 注解文件不存在: {anno_path}")
            return
        
        # 读取注解文件
        csv_dict = {}
        idx = 0
        valid_rows = 0
        
        with open(anno_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            
            for row_num, row in enumerate(csv_reader):
                if len(row) < 3:
                    continue
                
                try:
                    # 解析分数数据
                    score_values = [int(i) for i in row[2].split(',')]
                    video_id = str(idx // 20 + 1)  # 每20行对应一个视频
                    
                    if video_id in ids:
                        if idx % 20 == 0:
                            csv_dict[video_id] = np.array(score_values) / 20.0
                        else:
                            if video_id in csv_dict:
                                csv_dict[video_id] += np.array(score_values) / 20.0
                            else:
                                csv_dict[video_id] = np.array(score_values) / 20.0
                        
                        valid_rows += 1
                    
                    idx += 1
                    
                except (ValueError, IndexError) as e:
                    print(f"警告: 解析第{row_num}行时出错: {e}")
                    continue
        
        print(f"成功处理 {valid_rows} 行注解数据")
        print(f"有效的视频ID: {list(csv_dict.keys())}")
        
        if not csv_dict:
            print("错误: 没有有效的注解数据")
            return
        
        # 设置样式
        sns.set_style("whitegrid")
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 根据视频数量调整布局
        n_videos = len(ids)
        ncols = min(3, n_videos)
        nrows = (n_videos + ncols - 1) // ncols
        
        # 创建图形
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols, 4*nrows))
        fig.suptitle('视频关键帧得分分布图', fontsize=16, fontweight='bold')
        
        # 如果只有一个子图，确保axes是数组形式
        if n_videos == 1:
            axes = np.array([axes])
        if axes.ndim == 1:
            axes = axes.reshape(1, -1)
        
        # 为每个视频创建子图
        for i, video_id in enumerate(ids):
            row = i // ncols
            col = i % ncols
            
            if video_id in csv_dict:
                scores = csv_dict[video_id]
                
                # 获取预测摘要信息
                pred_summary = json_dict.get(video_id, {}).get('pred_summary', [])
                
                # 调试信息：打印数据长度和关键帧数量
                print(f"视频 {video_id}: 得分数组长度={len(scores)}, 关键帧数组长度={len(pred_summary)}")
                if len(pred_summary) > 0:
                    keyframe_count = sum(pred_summary)
                    print(f"视频 {video_id}: 关键帧数量={keyframe_count}/{len(pred_summary)}")
                
                # 确保pred_summary长度与scores匹配
                if len(pred_summary) != len(scores):
                    min_len = min(len(pred_summary), len(scores))
                    if min_len == 0:
                        print(f"警告: 视频 {video_id} 的pred_summary或scores为空")
                        # 尝试从HDF5文件获取视频实际帧数
                        video_key = 'video_' + video_id
                        if video_key in f_data:
                            cps = f_data[video_key]['change_points'][()]
                            if len(cps) > 0:
                                actual_frames = cps[-1][1]  # 最后一个变更点的结束帧
                                min_len = min(actual_frames, len(scores), len(pred_summary))
                                print(f"使用实际帧数调整: {actual_frames} -> 使用 {min_len} 帧")
                    
                    if min_len > 0:
                        pred_summary = pred_summary[:min_len]
                        scores = scores[:min_len]
                    else:
                        print(f"警告: 视频 {video_id} 无法确定有效帧数，跳过")
                        continue
                
                # 创建颜色数组 - 修复关键帧显示问题
                # 确保pred_summary是0/1数组，1表示关键帧
                colors = []
                for j, flag in enumerate(pred_summary):
                    # 确保flag是整数且为0或1
                    if isinstance(flag, (int, float)):
                        flag_int = int(flag)
                        if flag_int == 1:  # 关键帧
                            colors.append('orange')
                        else:  # 非关键帧
                            colors.append('lightseagreen')
                    else:
                        # 如果数据类型异常，默认使用非关键帧颜色
                        colors.append('lightseagreen')
                
                # 如果颜色数组长度不匹配，使用默认颜色
                if len(colors) != len(scores):
                    print(f"警告: 颜色数组长度不匹配，使用默认颜色")
                    colors = ['lightseagreen'] * len(scores)
                
                # 绘制条形图
                x_positions = np.arange(len(scores))
                bars = axes[row, col].bar(x_positions, scores, color=colors, 
                                        edgecolor='gray', linewidth=0.5, alpha=0.8, width=1.0)
                
                # 设置图表属性
                axes[row, col].set_title(f'视频 {video_id}', fontsize=12, fontweight='bold')
                axes[row, col].set_xlabel('帧索引')
                axes[row, col].set_ylabel('得分')
                
                # 设置合理的x轴范围，避免显示异常大的帧索引
                if len(scores) > 0:
                    axes[row, col].set_xlim(0, min(len(scores), 10000))  # 限制最大显示10000帧
                
                # 设置网格样式
                axes[row, col].grid(True, alpha=0.3, color='lightgray')
                
                # 添加图例（只在第一个子图添加）
                if i == 0:
                    from matplotlib.patches import Patch
                    legend_elements = [
                        Patch(facecolor='orange', label='关键帧'),
                        Patch(facecolor='lightseagreen', label='非关键帧')
                    ]
                    axes[row, col].legend(handles=legend_elements, loc='upper right')
                
                # 打印关键帧统计信息
                if len(pred_summary) > 0:
                    keyframe_indices = [j for j, flag in enumerate(pred_summary) if flag == 1]
                    print(f"视频 {video_id}: 关键帧位置示例: {keyframe_indices[:10] if len(keyframe_indices) > 10 else keyframe_indices}")
            else:
                axes[row, col].text(0.5, 0.5, f'视频 {video_id}\n无数据', 
                                   ha='center', va='center', transform=axes[row, col].transAxes)
                axes[row, col].set_title(f'视频 {video_id}')
        
        # 隐藏多余的子图
        for i in range(n_videos, nrows * ncols):
            row = i // ncols
            col = i % ncols
            axes[row, col].set_visible(False)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        
        # 保存图片
        save_path = os.path.join(save_dir, 'result-bar.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 条形图已保存: {save_path}")
        print(f"✓ 包含 {len([vid for vid in ids if vid in csv_dict])}/{len(ids)} 个视频的数据")
        
    except Exception as e:
        print(f"生成条形图时发生错误: {e}")
        import traceback
        traceback.print_exc()

def gen_summary():
    """生成摘要"""
    try:
        # 加载HDF5文件
        f_data = h5py.File(h5_path, 'r')
        
        # 加载JSON预测结果
        with open(json_path) as f:
            json_dict = json.load(f)
            ids = list(json_dict.keys())
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 获取视频文件列表并排序
        video_files = sorted([f for f in os.listdir(video_dir) if f.endswith('.mp4')])
        print(f"找到 {len(video_files)} 个视频文件")
        print(f"JSON中有 {len(ids)} 个视频ID需要处理")
        
        # 显示前几个文件的映射关系
        print("\n视频文件与ID的映射关系 (前10个):")
        for i, video_file in enumerate(video_files[:10]):
            video_id = str(i + 1)
            if video_id in ids:
                status = "✓"
            else:
                status = "✗"
            print(f"{status} {video_file} -> video_{video_id}")
        
        success_count = 0
        total_count = len(ids)
        
        print(f"\n开始处理 {total_count} 个视频...")
        
        for id in ids:
            print(f"\n处理视频 {id}...")
            
            try:
                # 将ID转换为整数索引
                id_int = int(id)
                if id_int < 1 or id_int > len(video_files):
                    print(f"错误: ID {id} 超出范围 (1-{len(video_files)})")
                    continue
                
                # 获取对应的视频文件名（索引从0开始）
                video_filename = video_files[id_int - 1]
                video_path = os.path.join(video_dir, video_filename)
                
                print(f"映射: video_{id} -> {video_filename}")
                
                if get_keys(id, video_path, f_data, json_dict):
                    success_count += 1
                    print(f"视频 {id} 处理成功")
                else:
                    print(f"视频 {id} 处理失败")
                    
            except ValueError:
                print(f"错误: ID {id} 不是有效的数字")
            except Exception as e:
                print(f"处理视频 {id} 时发生未知错误: {e}")
        
        print(f"\n处理完成: {success_count}/{total_count} 个视频成功处理")
        
        # 无论bar参数如何，总是尝试生成条形图
        if success_count > 0:
            print("生成分数条形图...")
            plot_bar(json_dict, ids, f_data)
        else:
            print("没有成功处理的视频，跳过条形图生成")
        
        f_data.close()
        
    except Exception as e:
        print(f"程序执行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    plt.switch_backend('agg')
    gen_summary()
