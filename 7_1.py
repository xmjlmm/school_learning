class Rectangle:
    def  __init__(self,x,y,width,height):
        self.X=x
        self.Y=y
        self.Width=width
        self.Height=height
        print("构造函数已执行")
    def getArea(self):
        s=self.Width*self.Height
        return s
    def pointInRect(self,x,y):
        x2=self.X+self.Width
        y2=self.Y+self.Height
        if(x>self.X and x<x2 and y>self.Y and y<y2):
            return True
        else:
            return False
def main():
    r1=Rectangle(0,0,100,100)
    print("矩形x:0,y:0,width:100,height:100")
    print("矩阵面积：",r1.getArea())
    x,y=eval(input("请输入一对坐标（逗号分隔）："))
    print("点（50，50）是否在矩阵内：",r1.pointInRect(x,y))
main()
