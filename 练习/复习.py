class Retangle:
    def __init__(self,x,y,width,height):
        self.X=x
        self.Y=y
        self.Width=width
        self.Height=height

    def getArea(self):
        Area=self.Height*self.Width
        return Area

    def pointInsert(self,x,y):
        x2=self.X+self.Width
        y2=self.Y+self.Height
        if(x>self.X and x<x2 and y>self.Y and y<y2):
            return True
        return False

def main():
    r=Retangle(0,0,100,100)
    print("矩阵x:0,y:0,width:100,height:100")
    print("矩阵面积:",r.getArea())
    x,y=eval(input("请输入一对坐标（逗号隔开）："))
    print("点(50,50)是否在矩阵内:",r.pointInsert(x,y))
main()