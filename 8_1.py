import random
IstData=[]
for i in range(0,10):
    x=random.randint(1,100)
    IstData.append(x)
i=0
while(i<len(IstData)):
    print(IstData[i],end="  ")
    i=i+1
maxi=0
i=1
while(i<len(IstData)):
    if(IstData[i]>IstData[maxi]):
        maxi=i
    i+=1
print("\n最大元素下标：",maxi)
print("最大元素值：",IstData[maxi])
mini=0
i=1
while(i<len(IstData)):
    if(IstData[i]<IstData[mini]):
        mini=i
    i+=1
print("最小元素下标：",mini)
print("最小元素值：",IstData[mini])
IstData[maxi],IstData[mini]=IstData[mini],IstData[maxi]
print(IstData)
