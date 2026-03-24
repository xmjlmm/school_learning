def fib(n):
    if (n==1 or n==2):
        return 1
    else:
        return fib(n-1)+fib(n-2)
def main():
    for n in range(1,41):
        print('{:>10}'.format(fib(n)), end='')
        if (n %8==0):
            print()
main()