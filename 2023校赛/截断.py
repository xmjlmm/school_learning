import pandas as pd

# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/dataid44.xlsx"
'''
Excel文件的路径分别为
"C:/Users/86159/Desktop/dataid3.xlsx"
"C:/Users/86159/Desktop/dataid8.xlsx"
"C:/Users/86159/Desktop/dataid28.xlsx"
"C:/Users/86159/Desktop/dataid30.xlsx"
"C:/Users/86159/Desktop/dataid44.xlsx"
'''

# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
data = pd.read_excel(file_path, engine='openpyxl')

# 显示数据长度
print(len(data))

# 截断信号数据
window_length = 500  # 截断窗口的长度
num_windows = len(data) // window_length  # 计算可以得到的窗口数量

# 提取截断后的信号数据
truncated_signal = []
for i in range(int(num_windows*0.6)):
    start = i * window_length
    end = (i + 1) * window_length
    window1 = data.loc[start:end, 'breath'].values
    window2 = data.loc[start:end, 'heart_rate'].values
    window3 = data.loc[start:end, 'totalMotion'].values
    window4 = data.loc[start:end, 'var'].values
    window5 = data.loc[start:end, 'average'].values
    window6 = data.loc[start:end, 'kurt'].values
    # 将四个窗口的数据转换为Series对象
    window1 = pd.Series(window1)
    window2 = pd.Series(window2)
    window3 = pd.Series(window3)
    window4 = pd.Series(window4)
    window5 = pd.Series(window5)
    window6 = pd.Series(window6)
    # 将四个窗口的数据按列连接
    window_data = pd.concat([window1, window2, window3, window4, window5, window6], axis=1)
    truncated_signal.append(window_data)
'''
# 输出截断后的信号数据
for i, window in enumerate(truncated_signal):
    print(f"Window {i+1}: {window}")
'''

# 将数据转换为DataFrame对象
df = pd.concat(truncated_signal)

# 导出数据到Excel文件
df.to_excel("C:/Users/86159/Desktop/dataid44(1).xlsx", index=False)
'''
导出数据到Excel文件的路径名称分别是
"C:/Users/86159/Desktop/dataid3(1).xlsx"
"C:/Users/86159/Desktop/dataid8(1).xlsx"
"C:/Users/86159/Desktop/dataid28(1).xlsx"
"C:/Users/86159/Desktop/dataid30(1).xlsx"
"C:/Users/86159/Desktop/dataid44(1).xlsx"
'''