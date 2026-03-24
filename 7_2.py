class BMI():
    def __init__(self,name,age,weight,height):
        self.Name=name
        self.Age=age
        self.Weight=weight
        self.Height=height
        print("构造已完成!")
    def getBMI(self):
        t=self.Weight/(self.Height**2)
        return t
    def getStatus(self):
        t=self.getBMI()
        if(t<18.5):
            return"偏瘦"
        elif(t<24):
            return"正常"
        elif(t<28):
            return"偏胖"
        else:
            return"实在太胖了，该减肥了"
    def setWeight(self,weight):
        self.Weight=weight
    def getWeight(self):
        return self.Weight
    def setHeight(self,height):
        self.Height=height
    def getHeight(self):
        return self.Height
def main():
    zs=BMI("张三",19,85,1.8)
    print("张三的身高为",zs.getHeight(),end="")
    print("体重为",zs.getWeight(),end="")
    print(" BMI数值是：",(zs.getBMI()),end="")
    print("状态为",zs.getStatus())
    print("经过一段时间的减肥....")
    zs.setWeight(75)
    print("请输入体重：75")
    print("经过一段时间的生长....")
    print("张三的BMI数值是：",zs.getBMI(),end="")
    print("状态为",zs.getStatus())
main()