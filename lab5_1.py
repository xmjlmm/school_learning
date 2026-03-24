import math
def isPrime(n):
    if n<2:
        return False
    t=int(math.sqrt(n))
    i=2
    while i<=t:
        if n%i==0:
            return False
        i=i+1
    return True

def main():
    for n in range(2,201):
        if isPrime(n)==True:
            print('{:>8}'.format(n),end='')
main()