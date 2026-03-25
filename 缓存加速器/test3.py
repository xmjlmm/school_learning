'''
不要在非确定性函数中使用缓存
当函数中包含任何非确定性内容时，我们绝对不能使用缓存。
还是用上面计算平均温度的例子来说明。
假设我们将需求修改为“获取今天的平均温度”。
我们可能需要在此函数中添加一个datetime.now()来获取当前的时间戳。
获取当前时间戳的行为是非确定性的。
'''

from datetime import datetime
from functools import cache

@cache
def get_current_time_cached():
    return datetime.now()
# 上述函数是最简单的非确定性函数。在运行函数之前，我们先运行 datetime.now() 函数获取当前时间戳。

print(get_current_time_cached())
print(get_current_time_cached.cache_info())
