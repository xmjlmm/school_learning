def binToDec(bin):
    n = len(bin)
    s=0
    for i in range(0,n):
        s=s+int(bin[i:i+1])*(2**(n-i-1))
    return s

def decToBin(dec):
    s=""
    if(dec==0):
        s="0"
    while dec!=0:
        s=str(dec%2)+s
        dec=dec//2
    return s

def main():
    print("十进制0~7对应的二进制数是：")
    print("{:>10}{:>10}".format("DEC","BIN"))
    for n in range(0,8):
        print("{:>10}{:>10}".format(n,decToBin(n)))

    print()
    print("二进制0~111对应的十进制数是：")
    print("{:>10}{:>10}".format("BIN","DEC"))
    for n in range(0,8):
        t=decToBin(n)
        print("{:>10}{:>10}".format(t,binToDec(t)))

main()
