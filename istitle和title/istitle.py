'''istitle() 方法用于检查字符串是否符合标题文本的格式，
即每个单词的首字母都是大写字母，其余字母都是小写字母或不是字母。
如果字符串符合标题文本格式，则返回 True，否则返回 False。'''


# Python istitle() method example
# 变量声明
str = "Welcome To Learnfk"
# 函数调用
str2 = str.istitle()
# 显示结果
print(str2)

# Python istitle() method example
# 变量声明
str3 = "Welcome To Learnfk" # True
# 函数调用
str4 = str3.istitle()
# 显示结果
print(str4)
str5 = "hello learnfk"    # False
str6 = str5.istitle()
print(str6)



