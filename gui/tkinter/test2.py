import tkinter

class app(object):
    def __init__(self, master):
        frame = tkinter.Frame(master)
        frame.pack()
        self.button = tkinter.Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side = tkinter.LEFT)
        self.hi_there = tkinter.Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side = tkinter.LEFT)

    def say_hi(self):
        print("hi there, this is a class example!")

win = tkinter.Tk()
app = app(win)
win.mainloop()


#!/usr/bin/python3
#-*- encoding=UTF-8 -*-
import tkinter as tk
root = tk.Tk()

def hello():
    print('hello')

def about():
    print('我是开发者')

menubar = tk.Menu(root)

# 创建下拉菜单File，然后将其加入到顶级的菜单栏中
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# 创建另一个下拉菜单Edit
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit",menu=editmenu)
# 创建下拉菜单Help
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

# 显示菜单
root.config(menu = menubar)

tk.mainloop()