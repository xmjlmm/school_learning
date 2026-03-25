# 暴力搜索模式串在文本串出现的位置

txt = input('请输入文本串')
pat = input('请输入模式串')
n = len(txt)
m = len(pat)
def bf(n, m):
    # 剪枝
    if n <= 0 or m <= 0:
        return -1
    i, j = 0, 0
    while i <= n and j <= m:
        if j >= m:
            return i - m
        if i >= n:
            return -1
        if txt[i] == pat[j]:
            i = i + 1
            j = j + 1
        else:
            i = i - j + 1
            j = 0

print(bf(n, m))


