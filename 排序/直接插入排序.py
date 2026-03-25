# 编写一个python程序，使用直接插入排序对数组进行排序

def insertion_sort(ls):
    length = len(ls)
    for i in range(1, length):
        for j in range(0, i):
            if ls[j] > ls[i]:
                ls.insert(j, ls[i])
                del ls[i+1]
    return ls

if __name__ == '__main__':
    ls = [1, 4, 2, 11, 6, 31, 52, 53, 2, 1, 8, 10, 9, 95, 280, 41, 4801, 489, 483, 491]
    ans = insertion_sort(ls)
    print(ans)
