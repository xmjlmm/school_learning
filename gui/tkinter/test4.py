import tkinter


win = tkinter.Tk(className = 'hello')

def next_num():
    next_num.count += 1
    label.config(text=f'Click count: {next_num.count}')
    button['text'] = 'next number is ' + str(next_num.count)
    print('count is', next_num.count)


# 函数的全局变量
next_num.count = 0

label = tkinter.Label()
label['text'] = 'hello'
label['fg'] = 'red'
label.pack()

button = tkinter.Button()
button['text']= 'Hello World'
button['command'] = next_num
button.pack(side = tkinter.RIGHT)

win.mainloop()