

while ():
    a, b = input('').split(' ')
    a = float(a)
    b = float(b)

    if (b!=0):
        c = a/b
        print("{:.2f}".format(c))
        print(end = '\n')
    else:
        print("error\n")

