'''
a=str(input())
if a>="0" and a<="100":
    print("1")
elif a<"0" or a>"100":
    print("2")
else:
    print("3")


'''






def gcd(m,n):
    if (m<n):
        m,n=n.m
    while n>0:
        t = m%n
        m = n
        n = t
    return m

def main():
    m = int(input('m='))
    n = int(input('n='))
    print(gcd(m,n))
main()