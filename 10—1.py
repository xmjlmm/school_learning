import math
class Shape:
    def __init__(self,color,filled):
        self.Color=color
        self.Filled=filled
    def __str__(self):
        return "Shape:Color:{},Filled:{}".format(self.Color,self.Filled)

class Triangle(Shape):
    def __init__(self,a,b,c):
        #print("自动调用函数")
        self.A=a
        self.B=b
        self.C=c
        super(). __init__("red",True)
    def getArea(self):
        p=(self.A+self.B+self.C)/2
        s=math.sqrt(p*(p-self.A)*(p-self.B)*(p-self.C))
        return s
    def __str__(self):
        return "Triangle:color:{},filled:{},a:{},b:{},c:{},面积={}".format(self.Color,self.Filled,self.A,self.B,self.C,self.getArea())

def main():
    sh=Shape("Green",False)
    print(sh)
    tr=(Triangle(3,4,5))
    print(tr)
main()