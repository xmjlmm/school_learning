import turtle
import time
import random


# 绘制彩灯
def draw_light():
    if random.randint(0, 30) == 0:
        color = 'red'
    elif random.randint(0, 30) == 1:
        color = 'yellow'
    elif random.randint(0, 30) == 2:
        color = 'blue'
    else:
        color = 'green'
    return color


# 绘制树
def draw_tree(t, branch_len):
    if branch_len > 5:
        if branch_len < 20:
            t.pencolor(draw_light())
            t.pensize(random.randint(4, 6))
            t.down()
            t.forward(branch_len)
            t.right(20)
            draw_tree(t, branch_len - 10)
            t.left(40)
            draw_tree(t, branch_len - 10)
            t.right(20)
            t.backward(branch_len)
            t.pensize(2)
        else:
            t.pencolor(draw_light())
            t.pensize(random.randint(4, 6))
            t.down()
            t.forward(branch_len)
            t.right(20)
            draw_tree(t, branch_len - 15)
            t.left(40)
            draw_tree(t, branch_len - 15)
            t.right(20)
            t.backward(branch_len)
            t.pensize(2)


# 绘制树干
def draw_trunk(t):
    t.pencolor("brown")
    t.pensize(30)
    t.down()
    t.right(90)
    t.forward(40)


# 绘制雪花
def draw_snow():
    t = turtle.Turtle()
    t.hideturtle()
    t.pensize(2)
    for i in range(200):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        t.pencolor(r, g, b)
        t.penup()
        t.setx(random.randint(-350, 350))
        t.sety(random.randint(-100, 350))
        t.pendown()
        dens = random.randint(8, 12)
        snowsize = random.randint(10, 14)
        for j in range(dens):
            t.forward(snowsize)
            t.backward(snowsize)
            t.right(360 / dens)


# 绘制字母
def draw_letters(t, word):
    colors = ["red", "yellow", "blue", "green", "white"]
    x = -50
    y = 200
    for char in word:
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.pencolor(random.choice(colors))
        t.write(char, font=("Arial", 30, "bold"))
        x += 40


# 星星闪烁效果
def draw_star(t):
    colors = ["yellow", "white"]
    t.penup()
    t.goto(0, 250)
    t.pendown()
    for i in range(30):
        t.pencolor(random.choice(colors))
        t.begin_fill()
        for j in range(5):
            t.forward(20)
            t.right(144)
        t.end_fill()
        t.right(12)


# 主函数
def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.bgcolor("black")
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.backward(100)
    t.left(90)
    t.backward(300)
    t.pendown()
    draw_tree(t, 100)
    draw_trunk(t)
    draw_snow()
    letter_turtle = turtle.Turtle()
    letter_turtle.hideturtle()
    draw_letters(letter_turtle, "bst")
    star_turtle = turtle.Turtle()
    star_turtle.speed(0)
    draw_star(star_turtle)
    turtle.done()


if __name__ == "__main__":
    import random
    main()