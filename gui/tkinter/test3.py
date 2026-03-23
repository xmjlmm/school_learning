import tkinter

# 这是窗口名字
win = tkinter.Tk(className = 'hello world')
win.geometry('400x300')

# # 加载图片
# image_source = "F:\ich liben dich\31ae08fde6f80cc01e3f7c2cc9547a3.png"
# bg_image = tkinter.PhotoImage(file = image_source)
#
# # 创建 Canvas 组件，并将背景图片绘制在 Canvas 上
# canvas = tkinter.Canvas(win, width=400, height=300)
# canvas.pack()


label = tkinter.Label(win, text = 'hello world', font = ('Arial', 12))
label.pack()

def next_num():
    # 输出打印这是第几次点击这个按钮
    next_num.count += 1
    label.config(text=f'Click count: {next_num.count}')
    print(f'Click count: {next_num.count}')



# 定义一个全局变量
next_num.count = 0

def print_hello():
    print('hello')

button = tkinter.Button()
button['text'] = 'click me'
button['command'] = next_num
button['height'] = 2
button['width'] = 10

button.pack(side = tkinter.RIGHT)

win.mainloop()