# 字符串要求字典序最小


def min_string(ls):
    for i in range(n-1):
        for j in range(0, n-i):
            length1 = len(ls[j])
            length2 = len(ls[j+1])
            min_len = min(length2, length1)
            for k in range(min_len):
                if ls[j][k] > ls[j+1][k]:
                    ls[j], ls[j+1] = ls[j+1], ls[j]
                    break
    return ls


if __name__ == '__main__':
    n = int(input())
    ls = []
    for _ in range(n):
        ls.append(input())



