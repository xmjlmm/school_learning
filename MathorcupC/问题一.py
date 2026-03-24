import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# 读取数据
data = pd.read_excel("F:\\数模\\2024年国赛复习资料\\论文\\MathorCupC\\C题\\附件\\附件1.xlsx")

# 确保日期列是 datetime 类型
data['日期'] = pd.to_datetime(data['日期'])

for center in data['分拣中心'].unique():
    center_data = data[data['分拣中心'] == center]
    center_data = center_data[['日期', '货量']].rename(columns={'日期': 'ds', '货量': 'y'})

    # 删除缺失值并确保数据有序
    center_data = center_data.dropna().sort_values(by='ds')

    if len(center_data) < 2:
        print(f"Not enough data for center {center}")
        continue

    # 定义节假日
    holidays = pd.DataFrame({
        'holiday': 'my_holidays',
        'ds': pd.to_datetime(['2024-01-01', '2024-12-25', '2024-11-11']),
        'lower_window': 0,
        'upper_window': 1,
    })

    # 初始化模型
    model = Prophet(holidays=holidays)  # Try different algorithms if needed

    try:
        # 训练模型
        model.fit(center_data)

        # 创建未来日期数据框并进行预测
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        # 绘制预测结果
        fig = model.plot(forecast)
        plt.title(f'Forecast for {center}')
        plt.show()
    except Exception as e:
        print(f"An error occurred for center {center}: {e}")
