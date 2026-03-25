import geopandas as gpd
import matplotlib.pyplot as plt

# 读取GeoPandas自带的国际地图数据
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# 画出地图
world.plot()

# 显示地图
plt.show()