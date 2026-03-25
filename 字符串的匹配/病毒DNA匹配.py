# 病毒的模版串，人体的DNA文本串
txt = input('人体的DNA文本串：')
pat = input('病毒的模版串：')
n = len(txt)
m = len(pat)
pat = pat * 2

'''
# 1.使用BF算法
def BF(n, m, txt, pat):
    if n <= 0 or m <= 0:
        return -1
    i, j = 0, 0
    while i <= n and j <= m:
        if j >= m:
            return i - m
        if i >= n:
            return -1
        if pat_pat[j] == txt[i]:
            j = j + 1
            i = i + 1
        else:
            i = i - j + 1
            j = 0
ans = -1
for k in range(m):
    pat_pat = pat[k:k+m]
    ans = max(ans, BF(n, m, txt, pat_pat))
print(ans)
'''


# 2.使用KMP算法
def next(m, pat):
    next = [0] * m
    next[1] = 1
    for i in range(2, m):
        k = 1
        for j in range(1, i):
            if pat[0:j:1] == pat[i-j:j:1]:
                k = max(k, j+1)
        next[i] = k
    return next

def nextval(next, pat):
    nextval = next.copy()
    nextval[0] = 0
    nextval[1] = 1
    for i in range(2, m):
        if pat[i] == pat[nextval[i] - 1]:
            nextval[i] = nextval[next[i] - 1]
    return nextval


def KMP(n, m, txt, pat, next):
    if n <= 0 or m <= 0:
        return -1
    i, j = 0, 0
    while i < n and j < m:
        if txt[i] == pat[j]:
            i, j = i + 1, j + 1
        elif j != 0:
            j = next[j - 1]
        else:
            i = i + 1
        if j == m:
            return i - m
    return -1  # 没找到

ans = [-1]
for k in range(m):
    pat_pat = pat[k:k+m]
    ls = next(m, pat_pat)
    ls_val = nextval(ls, pat_pat)
    ans.append(KMP(n, m, txt, pat_pat, ls_val))
    print(pat_pat)
    print(ls)
    print(ls_val)
    print(ans)
    print('----------------------')

ans = set(ans)
ans = list(ans)
ans.sort()
if len(ans) == 1:
    print(-1)
else:
    print(ans[1])


