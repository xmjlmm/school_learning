y=int(input("请输入年份为："))
if y%4==0 and y%100!=0 or y%400==0:
    print("{}是闰年".format(y))
else:
    print("{}不是闰年".format(y))
