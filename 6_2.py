import random
import turtle
def drawShape(n,length):
    i=0
    while i<n:
        turtle.pencolor(random.random(),random.random(),random.random())
        turtle.setheading(i*360/n)
        turtle.forward(length)
        i+=1
def main():
    n, length = eval(input("请输入边长数和边长（逗号隔开）："))
    turtle.setup(600,600)
    turtle.pensize(10)
    turtle.penup()
    x=random.random()*400-200
    y=random.random()*400-200
    turtle.goto(x,y)
    turtle.pendown()
    drawShape(n,length)
main()