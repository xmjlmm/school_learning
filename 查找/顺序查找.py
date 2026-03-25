# 编写Python代码，实现顺序表的查找操作。

# 哨兵顺序查找
def sqList(ls, key):
    ls.insert(0, key)
    length = len(ls)
    for i in range(length-1, -1, -1):
        if ls[i] == key:
            return i - 1
# 空间复杂度：一个辅助空间————O(1)
# 时间复杂度：O(n)
# ASL(n) = (1+2+...+n)/n = (n+1)/2 = O(n)  平均查找长度

# 常规顺序查找
def List(ls, key):
    length = len(ls)
    for i in range(length):
        if ls[i] == key:
            return i
    return -1

ls = [1, 2, 3, 4, 5, 6, 6, 9]
key = int(input('请输入需要查找的值：'))
ans = List(ls, key)
res = sqList(ls, key)
print(res)
print(ans)