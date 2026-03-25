import pandas as pd
import seaborn as sns
# from sklearn.datasets import load_iris
from tqdm import tqdm

# 导入鸢尾花数据集
# iris = load_iris()
# 加载数据集
df = pd.read_excel(r"C:\Users\86159\Desktop\绩点.xlsx")
# df = sns.load_dataset('iris')
# print(iris.data)
out = df.绩点.apply(lambda x: x*2)
print(out)

tqdm.pandas()
out1 = df.绩点.progress_apply(lambda x: x*2)
# print(out1)


