'''1.编写一个算法，将非负的十进制整数转换为其他进制的数输出，10及其以上的数字从‘A’开始的字母表示。
要求：
1) 采用顺序栈实现算法；
2）从键盘输入一个十进制的数，输出相应的八进制数和十六进制数。'''
# 由于十六进制数包含字母,所以需要打表或者利用ASCll码转换,打表浪费空间
def dec2binary(n, binary):
    stack = []
    res = ''
    while n > 0:
        stack.append(n % binary)
        n = n // binary
    while stack:
        if stack[-1] >= 10:
            stack[-1] = chr(stack[-1] + 55)
        res = res + str(stack.pop())
    return res

if __name__ == '__main__':
    n = int(input('请输入一个十进制的数：'))
    print('八进制的转换结果为：',dec2binary(n, 8))
    print('十进制的转换结果为：',dec2binary(n, 16))