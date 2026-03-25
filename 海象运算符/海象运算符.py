'''
海象运算符（walrusoperator）是Python
中引入的一种新的语法，其使用方法如下：

variable := expression
其中，expression是一个任意的表达式，
而variable则是一个变量名。
该运算符允许将表达式的结果赋值给变量，并且在同一行中进行这两个操作。
'''

def repeat_input():
    while (input_str := input('请输入：')) != 'exit':
        print(f"您输入的是{input_str}")
    return

def repeat_decide():
    my_list = [1, 2, 3, 4, 5]

    if (length := len(my_list)) > 0:
        print(f"列表中有{length}个元素！")

def rep_divideto():
    my_list = [1, 2, 3, 4, 5]

    # double_list = [x * 2 for x in my_list if (size := x * 2) > 3]
    double_list = [x * 2 for x in my_list if (length := len(my_list)) > 3]
    print(double_list)

def main():
    # repeat_input()
    repeat_decide()
    rep_divideto()

if __name__ == "__main__":
    main()