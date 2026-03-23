#计算1到100之间的偶数和
a=1
sum=0
while a<101:
    if a%2==0:
        sum+=a
    a+=1
print('1-100之间的偶数和',sum)

