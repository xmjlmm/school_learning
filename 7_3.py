class Stock():
    def __init__(self,symbol,name,previousClosingPrice,currentPrice):
        self.Symbol=symbol
        self.Name=name
        self.PreviousClosingPrice=previousClosingPrice
        self.CurrentPrice=currentPrice
        print("构造已完成！")
    def getStock(self):
        t=(self.CurrentPrice-self.PreviousClosingPrice)/self.PreviousClosingPrice
        t=round(t*100,2)
        return t
    def setSymbol(self,symbol):
        self.Symbol=symbol
        return symbol
    def getName(self):
        return self.Symbol
    def setName(self,name):
        self.Name=name
    def getName(self):
        return self.Name
    def setPreviousClosingPrice(self,previousClosingPrice):
        self.PreviousClosingPrice=previousClosingPrice
    def getPreviousClosingPrice(self):
        return self.PreviousClosingPrice
    def setCurrentPrice(self,currentPrice):
        self.CurrentPrice=currentPrice
    def getCurrentPrice(self):
        return self.CurrentPrice
def main():
    stock=Stock("60","INTC",20.5,20.35)
    print(stock.getName(),end="")
    print(stock.getCurrentPrice(),end="")
    print(str(stock.getStock())+"%")
main()