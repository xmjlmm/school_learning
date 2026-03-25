'''设备内存受限时，不要使用缓存
Python将这些缓存结果存储在哪里？当然是在计算机内存中。
存储一个城市的平均温度，甚至100个城市的平均温度当然都是没问题的。
然而，如果我们想缓存过去一年中全球所有主要城市每小时的滚动平均温度，那就不是一个好主意了。

不过，只需强调一点，如果我们想缓存许多小结果，但担心结果集可能太多，那么使用 lru_cache 将是一个很不错的选择。
functools.lru_cache 是一个特别有用的装饰器，它提供了一个缓存机制，
可以存储最近使用过的结果，并在达到缓存限制时自动丢弃最少使用的数据。
这对于那些需要缓存大量但不希望无限增长内存使用的场景非常适合。

下面的例子展示了如何使用 lru_cache 来缓存一个计算函数的结果，
该函数计算过去一定时间范围内的温度滚动平均值。在这个例子中，我们模拟缓存多个城市每小时的温度滚动平均值。
'''
from functools import cache
import random

# 模拟获取某城市某小时的温度
def get_temperature(city, hour):
    return random.uniform(20, 30)

# 使用cache装饰器定义一个缓存温度平均值的函数
@cache  # 设定缓存大小为1000
def get_rolling_average(city, start_hour, end_hour):
    total_temp = 0
    count = end_hour - start_hour
    for hour in range(start_hour, end_hour):
        total_temp += get_temperature(city, hour)
    return total_temp / count

# 测试函数
# 获取并打印某城市连续多小时的温度平均值
city = "New York"
start_hour = 0
end_hour = 24
average_temp = get_rolling_average(city, start_hour, end_hour)
print(f"Average temperature from {start_hour} to {end_hour} in {city} is {average_temp:.2f}")

# 调用相同参数的函数多次以观察缓存效果
print(get_rolling_average(city, start_hour, end_hour))  # 直接从缓存中获取结果
print(get_rolling_average(city, start_hour + 1, end_hour + 1))  # 计算新的平均温度，并缓存结果

# 检查缓存的状态
print(get_rolling_average.cache_info())

'''CacheInfo 字段解释
hits:

表示缓存中成功命中的次数。即在进行缓存查询时，查询的键存在于缓存中，并且有效（未过期），这时命中数会增加。
misses:

表示缓存中未命中的次数。即在进行缓存查询时，查询的键不存在于缓存中，或者已过期，这时未命中数会增加。
maxsize:

缓存的最大容量限制。如果设置了缓存的最大容量，则 maxsize 表示该限制；如果没有设置，则为 None。
currsize:

当前缓存中的项数。即当前缓存中实际存储的键值对数量。'''