# 用python３创建窗口并显示
# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
#
# import tkinter
#
# top=tkinter.Tk()
#
# #进入消息循环体
# top.mainloop()
# print('#####################################################')


# # 修改窗口的名字
# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
#
# import tkinter
#
# top=tkinter.Tk(className='hello world')
#
# #进入消息循环体
# top.mainloop()
# print('#####################################################')


# # 在窗口中加入标签
# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
#
# import tkinter
#
# top=tkinter.Tk(className='hello world')
#
# #加上标签
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# #进入消息循环体
# top.mainloop()
# print('#####################################################')



# 在窗口中加入按钮
# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
#
# import tkinter
#
# top = tkinter.Tk(className='hello world')
#
# #加上标签
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# #加上按钮
# button = tkinter.Button(top)
# button['text'] = 'Ok'
# button.pack()
#
# #进入消息循环体
# top.mainloop()
# print('#####################################################')


# # 使按钮有实际意义
# import tkinter
#
# def on_click():
#     label['text'] = 'no way out'
#
# top = tkinter.Tk(className = 'helloworld')
#
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# button = tkinter.Button(top)
# button['text'] = 'Ok'
#
# button['command'] = on_click
# button.pack()
#
# top.mainloop()
# print('#####################################################')


# # 添加可编辑文本框
# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
#
# import tkinter
#
# def on_click():
#     label['text'] = 'no way out'
#
# top=tkinter.Tk(className='hello world')
#
# #加上标签
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# #加上按钮
# button = tkinter.Button(top)
# button['text'] = 'Ok'
# #添加按钮操作
# button['command'] = on_click
# button.pack()
#
# #添加可编辑文本框
# text = tkinter.StringVar()
# text.set('change to what?')
# entry = tkinter.Entry(top)
# entry['textvariable'] = text
# entry.pack()
#
# #进入消息循环体
# top.mainloop()
# print('#####################################################')


# # #!/usr/bin/python3
# # #-*-coding: UTF-8 -*-
# # 法1
# import tkinter
#
# def on_click():
#     print('hello world')
#
# top=tkinter.Tk(className='hello world')
# #定义窗体的大小，是400X200像素
# top.geometry('400x200')
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# #加上按钮
# button = tkinter.Button(top)
# button['text'] = 'click'
# #添加按钮操作
# button['command'] = on_click
# button.pack()
#
# #进入消息循环体
# top.mainloop()
# # print('#####################################################')



# #!/usr/bin/python3
# #-*-coding: UTF-8 -*-
# from tkinter import *   #引入Tkinter工具包
# def hello():
#     print('hello world!')
#
# win = Tk()  #定义一个窗体
# win.title('Hello World')    #定义窗体标题
# win.geometry('400x200')     #定义窗体的大小，是400X200像素
#
# btn = Button(win, text='Click me', command=hello)
# #注意这个地方，不要写成hello(),如果是hello()的话，会在mainloop中调用hello函数
# #会在mainloop中调用hello函数，
# # 而不是单击button按钮时出发事件
# btn.pack(expand=YES, fill=BOTH) #将按钮pack，充满整个窗体(只有pack的组件实例才能显示)
#
# win.mainloop() #进入主循环，程序运行


# import tkinter
#
# top = tkinter.Tk(className = 'hello world')
#
# def hello():
#     print('hello world')
#
# label = tkinter.Label(top)
# label['text'] = 'be on your own'
# label.pack()
#
# button = tkinter.Button(top)
# button['text'] = 'click'
# # button['command'] = lambda: print('hello world')
# button['command'] = hello
# button.pack(expand = True, fill = 'both')
#
# top.mainloop()

# # 添加２个按钮并改变按钮字体颜色
# #!/usr/bin/python3
# #-*-coding: UTF-8 -*-
#
# import tkinter
#
# class App:
#     def __init__(self, master):
#         # 构造函数里传入一个父组件(master),创建一个Frame组件并显示
#         frame = tkinter.Frame(master)
#         frame.pack()
#         # 创建两个button，并作为frame的一部分
#         self.button = tkinter.Button(frame, text="QUIT", fg="red", command=frame.quit)
#         self.button.pack(side=tkinter.LEFT) # 此处side为LEFT表示将其放置 到frame剩余空间的最左方
#         self.hi_there = tkinter.Button(frame, text="Hello", command=self.say_hi)
#         self.hi_there.pack(side=tkinter.LEFT)
#
#     def say_hi(self):
#         print("hi there, this is a class example!")
#
# win = tkinter.Tk()
# app = App(win)
# win.mainloop()

# import tkinter
#
# win = tkinter.Tk(className = 'hello')
#
# label = tkinter.Label(win)
# label['text'] = 'be on your own'
# label.pack()
#
# button1 = tkinter.Button(win)
# button1['text'] = 'QUIT'
# button1['fg'] = 'red'
# button1['command'] = win.quit
#
# button1.pack(side = tkinter.TOP)
# button2 = tkinter.Button(win)
# button2['text'] = 'Hello'
# button2['command'] = lambda: print('hello')
# button2.pack(side = tkinter.RIGHT)
#
# win.mainloop()



