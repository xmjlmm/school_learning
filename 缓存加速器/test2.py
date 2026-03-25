import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import cache

# 创建样本数据：记录5个城市10天内的每小时温度
np.random.seed(0)
date_range = pd.date_range(start='2024-04-01', end='2024-04-10', freq='h')
temp_df = pd.DataFrame({
    'timestamp': np.tile(date_range, 5),
    'city': np.repeat(['北京', '上海', '广州', '深圳', '天津'], len(date_range)),
    'temperature': np.random.normal(loc=15, scale=10, size=(len(date_range)*5, ))
})


def compute_avg_daily_temp(date, city):
    daily_temp_df = temp_df[(temp_df['timestamp'].dt.date == pd.to_datetime(date).date())
                             & (temp_df['city'] == city)]
    return daily_temp_df['temperature'].mean()

@cache
def compute_avg_daily_temp_cached(date, city):
    daily_temp_df = temp_df[(temp_df['timestamp'].dt.date == pd.to_datetime(date).date())
                            & (temp_df['city'] == city)]
    return daily_temp_df['temperature'].mean()

print(compute_avg_daily_temp('2024-04-01', '北京'))
print(compute_avg_daily_temp_cached('2024-04-01', '北京'))
print(compute_avg_daily_temp_cached.cache_info())
print(compute_avg_daily_temp_cached.cache_clear())