def duplicate(lst):
    i = 0
    n = len(lst)
    while (i <= n - 2):
        j = i + 1
        while (j <= n - 1):
            if (lst[i] == lst[j]):
                return True
            j = j + 1
        i = i + 1
    return False

def main():
    while True:

        lst = eval(input("请输入列表:"))
        if (len(lst) == 0):
            print("程序结束！")
            return
        print(duplicate(lst))
main()