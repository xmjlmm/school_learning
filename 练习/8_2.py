import random
print("列表a：")
def init(lst1,lst2):
    for i in range (0,20):
        x=random.randint(0,100)
        lst1.append(x)
    print(lst1)

def average(lst1,lst2):
    s=0
    for i in range (0,20):
        x=random.randint(0,100)
        s=s+x
    average=s/len(lst1)
    print("平均值是：",average)
    for i in range (0,20):
        if(lst1[i]>=average and lst1[i]%2==0):
            x=lst1[i]
            lst2.append(x)
    print("列表b:")
    print(lst2)

def main():
    a=[]
    b=[]
    init(a,b)
    average(a,b)
main()
