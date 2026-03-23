import turtle

turtle.setup(0.5, 0.5)
turtle.pencolor("red")
turtle.pensize(10)


def drawShapr(n, length):
    turtle.setheading(s * 72)
    turtle.forward(100)

n,length=eval(input("输入一对坐标（逗号分隔）："))
s = 0
for i in range(0, 5):
    drawShapr(n, length)
    s += 1
turtle.done()
