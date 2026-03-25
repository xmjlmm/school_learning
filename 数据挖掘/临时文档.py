'''
import numpy as np
import matplotlib.pyplot as plt

xs = np.arange(8)
series1 = np.array([1, 3, 3, None, None, 5, 8, 9]).astype(np.double)
s1mask = np.isfinite(series1)
series2 = np.array([2, None, 5, None, 4, None, 3, 2]).astype(np.double)
s2mask = np.isfinite(series2)

plt.plot(xs[s1mask], series1[s1mask], linestyle='-')
plt.plot(xs[s2mask], series2[s2mask], linestyle='-', marker='o')

plt.show()
'''
'''
n = int(input('输入'))
a = 1
b = 1
i = 1
s = 0
f = 1
x = a/b*f
for i in range(1,n+1):
    s=s+x
    f=-f
    b=b+2
    x=a/b*f
print(s)
print(3.14/4)
'''
'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris,make_moons,make_circles,make_blobs
from sklearn.metrics import silhouette_score,homogeneity_completeness_v_measure
from sklearn.cluster import KMeans
iris = load_iris()
iris_X = iris.data
iris_Y = iris.target
clf = KMeans(random_state = 123)
clf.get_params()
print(clf.get_params())
cif = KMeans(n_clusters = 3,n_init = 10,random_state = 123)
cif.fit(iris_X)
print(clf)
'''
'''
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.model_selection import KFold,GridSearchCV,train_test_split
iris = load_iris()
iris_X = iris.data
iris_y = iris.target
iris_train_X,iris_test_X,iris_train_y,iris_test_y = train_test_split(iris_X,iris_y,test_size = 0.2,random_state = 123)
df = DecisionTreeClassifier(max_depth = 3,min_impurity_decrease = 0.01,random_state =123)
print(df.fit(iris_train_X,iris_train_y))
'''
'''
def is_power(m, n):
    if m == 1:  # m为1时，任何数的整数次方都是1
        return True
    if m == n:  # m等于n时，m是n的1次方
        return True
    if n == 1 and m != 1:  # n为1时，除了m等于1，其他数的整数次方都不是1
        return False
    if m % n == 0:  # 如果m能整除n，继续递归判断m/n是否是n的整数次方
        return is_power(m // n, n)
    return False  # 其他情况都返回False

def main():
    m = int(input('请输入m的值为：'))
    n = int(input('请输入n的值为：'))
    print(is_power(m,n))
main()
'''

def analyze_lyrics(lyrics):
    word_counts = {}  # 用于记录词语出现的次数的字典

    # 去除换行符和空格，并按照空格分割歌词为单词列表
    words = lyrics.replace('\n', ' ').split()

    # 遍历歌词中的每个单词
    for i in range(len(words)-1):
        word = words[i] + words[i+1]  # 构造两个字的词语
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # 找到出现次数最多的词语
    max_count = max(word_counts.values())
    most_common_words = [word for word, count in word_counts.items() if count == max_count]

    return most_common_words, max_count

# 测试
lyrics = '''
高楼是你拔地的想象
街道是你动感的面庞
长桥是你华丽的首饰
霓虹是你奇幻的时装
人海是你超凡的自信
车流是你长远的目光
风景是你妩媚的阴柔
艺术是你传神的宝藏
亲爱的城市
我亲爱的城市
跟我一起爱你的是琴弦般的阳光
此刻我已变成一把 guitar
融入你美好的歌唱
亲爱的城市
我亲爱的城市
跟我一起爱你的是琴弦般的阳光
此刻我已变成一把 guitar
融入你美好的歌唱
'''
result = analyze_lyrics(lyrics)
print("最常出现的两个字的词语及出现的次数：")
for word in result[0]:
    print("{}: {}".format(word,result[1]))

'''
import jieba
lyrics = '''
高楼是你拔地的想象
街道是你动感的面庞
长桥是你华丽的首饰
霓虹是你奇幻的时装
人海是你超凡的自信
车流是你长远的目光
风景是你妩媚的阴柔
艺术是你传神的宝藏
亲爱的城市
我亲爱的城市
跟我一起爱你的是琴弦般的阳光
此刻我已变成一把 guitar
融入你美好的歌唱
亲爱的城市
我亲爱的城市
跟我一起爱你的是琴弦般的阳光
此刻我已变成一把 guitar
融入你美好的歌唱
'''
'''
lyrics = lyrics.replace('\n', '')
ls = jieba.lcut(lyrics)
print(ls)
'''