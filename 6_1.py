import math
n1=float(input("n1"))
n2=float(input("n2"))
n3=float(input("n3"))
av=(n1+n2+n3)/3
print(av)
cv=math.sqrt((n1-av)**2+(n2-av)**2+(n3-av)**2)/3
print(cv)