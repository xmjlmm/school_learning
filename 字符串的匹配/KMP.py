import time

# 使用KMP求解模板串在字符串中出现的位置
txt = input('请输入字符串为：')
pat = input('请输入模版串为：')
n = len(txt)
m = len(pat)

def next(m):
    # 求next数组
    next = [0] * m
    next[1] = 1
    for i in range(2, m):
        # 对于模板串求next数组
        k = 1
        for j in range(1, i):
            if pat[0:j:1] == pat[i-j:i:1]:
                k = max(k, j + 1)
        next[i] = k
    return next

def nextval(m, pat, next):
    nextval = next.copy()  # 用于保存nextval的结果
    nextval[0] = 0  # nextval数组的第一位是0
    nextval[1] = 1
    for i in range(2, m):
        if pat[i] == pat[nextval[i] - 1]:  # 如果前一位的最长公共前后缀的下一位和当前字符相等
            nextval[i] = nextval[next[i] - 1]
    return nextval

def KMP(n, m, nextval):
    # KMP算法基于nextval数组
    if n <= 0 or m <= 0:
        return -1
    i, j = 0, 0
    while i < n and j < m:
        if txt[i] == pat[j]:
            i, j = i + 1, j + 1
        elif j != 0:
            j = nextval[j - 1]
        else:
            i = i + 1
        if j == m:
            return i - m
    return -1  # 没找到

ls = next(m)
ls_val = nextval(m, pat, ls)

print(ls)
print(ls_val)
print(KMP(n, m, ls))
print(KMP(n, m, ls_val))

