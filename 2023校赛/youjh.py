import pandas as pd
import random

# Load the data from Excel file
filename = "C:/Users/86159/Desktop/dataid44.xlsx"
sheet_name = 'Sheet1'
data_frame = pd.read_excel(filename, sheet_name=sheet_name)

# Assuming that your data is in the first column (column A)
column_name = data_frame.columns[0]
data = data_frame[column_name].tolist()

# Parameters
#start_index = 0  # specify the starting index for the subset
length = 300     # number of consecutive elements you want to extract

# Randomly select the starting index for the subset
start_index = random.randint(0, len(data) - length)
'''
# Extract the consecutive data
subset = data[start_index:start_index + length]

# Print the extracted data
print(subset)
'''
# 提取截断后的信号数据
truncated_signal = []
for i in range(start_index, start_index+length):
    window1 = data_frame.loc[i:i+1, 'breath'].values
    window2 = data_frame.loc[i:i+1, 'heart_rate'].values
    window3 = data_frame.loc[i:i+1, 'totalMotion'].values
    window4 = data_frame.loc[i:i+1, 'var'].values
    window5 = data_frame.loc[i:i+1, 'average'].values
    window6 = data_frame.loc[i:i+1, 'kurt'].values
    # 将四个窗口的数据转换为Series对象
    window1 = pd.Series(window1)
    window2 = pd.Series(window2)
    window3 = pd.Series(window3)
    window4 = pd.Series(window4)
    window5 = pd.Series(window5)
    window6 = pd.Series(window6)
    # 将四个窗口的数据按列连接
    window_data = pd.concat([window1, window2, window3, window4, window5, window6], axis=1,ignore_index=True)
    truncated_signal.append(window_data)
'''
# 输出截断后的信号数据
for i, window in enumerate(truncated_signal):
    print(f"Window {i+1}: {window}")
'''

# 将数据转换为DataFrame对象
df = pd.concat(truncated_signal)

# 导出数据到Excel文件
df.to_excel("C:/Users/86159/Desktop/data3.xlsx", index=False)