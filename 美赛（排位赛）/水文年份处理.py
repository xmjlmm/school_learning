'''
import pandas as pd

# 原始数据
df = pd.read_csv("D://数模//美赛//2023校赛//处理后data1.csv")
hydrological_years = pd.to_datetime(df['hydrological.year'])
start_years, end_years = [], []

length = len(hydrological_years)

for i in range(length):
    year = hydrological_years[i]
    year.split('/')
    start_year = int(year[0])
    end_year = int(year[1])
# 提取开始年份和结束年份


for i in range(len(start_years)):
    start_year = str(start_years[i])
    end_year = str(end_years[i])
    main = start_year[0:2]
    if main == '19':
        end_year = '19' + end_year
    else:
        end_year = '20' + end_year
    end_years[i] = int(end_year)

# 创建DataFrame
df = pd.DataFrame({'start_year': start_years, 'end_year': end_years})

# 打印DataFrame
df.to_excel("D://数模//美赛//2023校赛//1.xlsx")

'''

'''
import pandas as pd

# 原始数据
df = pd.read_csv("D://数模//美赛//2023校赛//处理后data1.csv")
hydrological_years = df['hydrological.year'].values
start_years, end_years = [], []

# 开始年份和结束年份提取
for year in hydrological_years:
    split_year = year.split('/')
    start_years.append(int(split_year[0]))
    end_years.append(int(split_year[1]))

# 创建新的DataFrame存储开始年份和结束年份
df_year = pd.DataFrame({'start_year': start_years, 'end_year': end_years})

# 将DataFrame写入excel文件
df_year.to_excel("D://数模//美赛//2023校赛//1.xlsx", index=False)
'''

'''
import pandas as pd

# 示例数据
data = pd.DataFrame({
    'Hydrological_Year': ['1970/71', '2000-1-1', '1985/86', '1999-12-31']
})
df = pd.read_csv("D://数模//美赛//2023校赛//处理后data1.csv")
hydrological_years = pd.to_datetime(df['hydrological.year'])
# 处理水文年份
def process_hydrological_year(hy_year):
    if '-' in hy_year:
        # 处理格式为 '2000-1-1'
        return pd.to_datetime(hy_year).year
    else:
        # 处理格式为 '1970/71'，取第一个年份
        return int(hy_year.split('/')[0])

# 应用函数转换水文年份
data['Processed_Hydrological_Year'] = data['Hydrological_Year'].apply(process_hydrological_year)

# 展示处理后的数据
print(data)
'''


import pandas as pd

# 原始数据
df = pd.read_excel("D://数模//美赛//2023校赛//2022.xlsx")
hydrological_years = df['hydrological.year']
start_years, end_years = [], []

# 开始年份和结束年份提取
for year in hydrological_years:
    split_year = year.split('/')
    start_years.append(int(split_year[0]))
    end_years.append(int(split_year[1]))

# 创建新的DataFrame存储开始年份和结束年份
df_year = pd.DataFrame({'start_year': start_years, 'end_year': end_years})

# 将DataFrame写入excel文件
df_year.to_excel("D://数模//美赛//2023校赛//1.xlsx", index=False)
