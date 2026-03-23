import tkinter

win = tkinter.Tk(className = 'hello')

def next_num():
    next_num.count += 1
    Label['text'] = "next_num.count" + str(next_num.count)
    button['text'] =  "click me" + str(next_num.count)
    print('next_num.count'+ str(next_num.count))
    button['command'] = next_num

next_num.count = 0

Label = tkinter.Label(text = 'hello')
Label.pack()

button = tkinter.Button(text = 'click me', command = next_num)
button.pack()

win.mainloop()