import pandas as pd

# 原始数据
hydrological_years = ['1970/71', '1971/72', '1972/73']   # 你可以按需添加更多的数据

# 提取开始年份和结束年份
start_years = [int(year.split('/')[0]) for year in hydrological_years]
end_years = [int(year.split('/')[1]) for year in hydrological_years]

# 创建DataFrame
df = pd.DataFrame({'start_year': start_years, 'end_year': end_years})

# 打印DataFrame
print(df)