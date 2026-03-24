import random
def init(lst):
    print("列表a:")
    for i in range(0,10):
        x=random.randint(1,100)
        lst.append(x)
    print(lst)

def change(arr):
    print("排序后:")
    for i in range(0,8):
        for j in range(0,9-i):
            if (arr[j]<arr[j+1]):
                t=arr[j]
                arr[j]=arr[j+1]
                arr[j+1]=t
    print(arr)

def main():
    arr=[]
    init(arr)
    change(arr)
main()