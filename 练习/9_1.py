import random
import math
def createPoints(lst):
    lst.clear()
    for i in range (0,10):
        p=[random.randint(-10,10),random.randint(-10,10)]
        lst.append(p)

def printPoints(lst):
    print("以下为10个点坐标：")
    for i in range (0,len(lst)):
        p=lst[i]
        print("({},{})".format(p[0],p[1]),end="")
    print()


def getDistance(x1,y1,x2,y2):
    d=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return d

def closestPoint(x,y,lst):
    p=lst[0]
    minD=getDistance(x,y,p[0],p[1])
    mini=0
    for i in range(1,len(lst)):
        p=lst[i]
        if (getDistance(x,y,p[0],p[1])<minD):
            minD=getDistance(x,y,p[0],p[1])
            mini=i
        p=lst[mini]
    return minD,mini,p

def main():
    pointList=[]
    createPoints(pointList)
    printPoints(pointList)
    x,y=eval(input("输入你的坐标(用逗号隔开):"))
    d,i,p=closestPoint(x,y,pointList)
    print("离你最近的点是:({},{})".format(p[0],p[1]),end="")
    print("距离是：",d)

main()