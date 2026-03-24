import random

print("随机生成的二维列表：")
arr=[]
for j in range(1, 4):
    cols = []
    for i in range(1, 4):
        x = random.randint(0, 9)
        cols.append(x)
    arr.append(cols)
print(arr)

print("打印为矩阵形式：")
s = 0
for i in range(0, 3):
    count = 0
    for j in range(0, 3):
        if ((i + j + 2) % 2 == 0):
            s = s + (arr[i - 1][j - 1])
        print(arr[i][j], end=" ")
        count += 1
        if (count % 3 == 0):
            print()
print('两条对角线元素之和为：', s)
