# import streamlit as st
# import pandas as pd
# import numpy as np
#
# st.title('Uber pickups in NYC')
#
# DATA_COLUMN = 'data/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#
#
# # 增加缓存
# @st.cache_data
# # 下载数据函数
# def load_data(nrows):
#     # 读取csv文件
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     # 转换小写字母
#     lowercase = lambda x: str(x).lower()
#     # 将数据重命名
#     data.rename(lowercase, axis='columns', inplace=True)
#     # 将数据以panda的数据列的形式展示出来
#     data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
#     # 返回最终数据
#     return data
#
#
# # 直接打印文本信息
# data_load_state = st.text('正在下载')
# # 下载一万条数据中的数据
# data = load_data(10000)
# # 最后输出文本显示
# data_load_state.text("完成！(using st.cache_data)")
#
# # 检查原始数据
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
#
# # 绘制直方图
# # 添加一个子标题
# st.subheader('Number of pickups by hour')
#
# # 使用numpy生成一个直方图，按小时排列
# hist_values = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# # 使用Streamlit 的 st.bar_chart（） 方法来绘制直方图
# st.bar_chart(hist_values)
#
# # 使用滑动块筛选结果
# hour_to_filter = st.slider('hour', 0, 23, 17)
# # 实时更新
# filtered_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]
#
# # 为地图添加一个副标题
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# # 使用st.map()函数绘制数据
# st.map(filtered_data)

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATA_COLUMN = 'Date/Time'  # 修改为正确的列名
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# 使用 @st.cache 装饰器缓存数据
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])  # 将时间列转换为 datetime 类型
    return data

# 下载数据并显示加载状态
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Data loaded successfully!")

# 展示原始数据的复选框
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 绘制小时统计的直方图
st.subheader('Number of pickups by hour')

# 使用numpy生成一个直方图，按小时排列
hist_values, bins = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))
st.bar_chart(hist_values, xticks=bins[:-1])

# 使用滑动块选择小时，并实时更新
hour_to_filter = st.slider('Select hour', 0, 23, 17)
filtered_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]

# 在地图上显示选定小时的所有点
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data[['Lat', 'Lon']].dropna())  # 假设数据包含纬度（Lat）和经度（Lon）
