import random

def init(lst, n, minVal, maxVal):
    for i in range(0, n):
        x = random.randint(minVal, maxVal)
        lst.append(x)
    print("列表a:\n", lst)

'''
一个一个输出列表元素
def printList(a):
    for i in range(0,len(a)):
        print(a[i],end="  ")
'''

def change(lst):
    maxi = 0
    mini = 0
    i = 1
    while (i < len(lst)):
        if (lst[i] > lst[maxi]):
            maxi = i
        if (lst[i] < lst[mini]):
            mini = i
        i += 1
    print("\n最大值为", lst[maxi], end="")
    print("下标为：", maxi)
    print("最小值为", lst[mini], end="")
    print("下标为：", mini)
    t=lst[maxi]
    lst[maxi]=lst[mini]
    lst[mini]=t
    print("交换最大值最小值的位置，交换后：\n", lst)

def main():
    a = []
    init(a, 10, 1, 100)
    # printList(a)
    change(a)

main()