import xalpha as xa
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
# 获取基金数据
zzyl = xa.fundinfo('021580')

# 筛选日期范围内的数据
start_date = '2025-06-30'
end_date = '2025-10-30'
filtered_data = zzyl.price[(zzyl.price['date'] >= start_date) & (zzyl.price['date'] <= end_date)]

# 查看筛选后的数据，确认数据格式
print("筛选后的数据前5行:")
print(filtered_data.head())
print("\n数据基本信息:")
print(filtered_data.info())

print(zzyl.get_stock_holdings(2025, 2))

# 核心设置：指定中文字体和解决负号显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']  # 指定一个字体列表，按优先级使用
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题[6,7](@ref)

# 绘图
plt.figure(figsize=(12, 6))

# 绘制单位净值曲线
plt.plot(filtered_data['date'], filtered_data['netvalue'], marker='o', linestyle='-', linewidth=1.5, markersize=3, label='单位净值 (netvalue)')

# 如果 totvalue 存在且与 netvalue 不同，则也绘制出来
if 'totvalue' in filtered_data.columns and not filtered_data['totvalue'].equals(filtered_data['netvalue']):
    plt.plot(filtered_data['date'], filtered_data['totvalue'], marker='s', linestyle='--', linewidth=1.5, markersize=3, label='累计净值/总价值 (totvalue)')
else:
    print("\n'累计净值/总价值 (totvalue)' 与 '单位净值 (netvalue)' 相同或不存在，仅绘制单位净值。")

# 添加标题和轴标签
plt.title(f'华夏人工智能ETF联接D (021580) 净值走势图 ({start_date} 至 {end_date})', fontsize=16)
plt.xlabel('日期', fontsize=12)
plt.ylabel('净值', fontsize=12)

# 设置日期格式
import matplotlib.dates as mdates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# 根据数据跨度调整主刻度间隔，例如每两周一个刻度
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
plt.xticks(rotation=45)

# 添加网格和图例
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# 自动调整布局防止重叠
plt.tight_layout()

# 显示图表
plt.show()