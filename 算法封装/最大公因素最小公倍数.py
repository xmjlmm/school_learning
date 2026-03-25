def gcd(a, b):
    # 将a, b中较大的数放在b中
    if a > b:
        a, b = b, a
    # 辗转相除法
    c = b % a
    while c:
        b = a
        a = c
        c = b % a
    return a

# 递归求最大公因数
def gcd2(a, b):
    return a if b == 0 else gcd2(b, a % b)


def pcd(a, b, c):
    return a * b // c

def main():
    a = 4
    b = 5
    c = gcd(a, b)
    c2 = gcd(a, b)
    print(c)
    print(c2)
    print(pcd(a, b, c))
    print(pcd(a, b, c2))

if __name__ == '__main__':
    main()
