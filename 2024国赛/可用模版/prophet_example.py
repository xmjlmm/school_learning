import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet

# 生成示例时间序列数据
def generate_sample_data():
    date_range = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    data = pd.DataFrame(date_range, columns=['ds'])
    data['y'] = 10 + 2 * np.sin(np.linspace(0, 3 * np.pi, len(date_range)))
    data['y'] += np.random.normal(scale=0.5, size=len(date_range))
    data = data.dropna()
    return data

# 创建和训练Prophet模型
def train_prophet_model(data):
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.1
    )
    model.fit(data)
    return model

# 进行预测
def make_forecast(model, periods=30):
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast

# 绘制预测结果
def plot_forecast(model, forecast):
    fig = model.plot(forecast)
    plt.title('Prophet 预测结果')
    plt.xlabel('日期')
    plt.ylabel('值')
    plt.show()

def main():
    data = generate_sample_data()
    model = train_prophet_model(data)
    forecast = make_forecast(model)
    plot_forecast(model, forecast)

if __name__ == "__main__":
    main()
