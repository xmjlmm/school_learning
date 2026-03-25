'''Python rstrip()方法从字符串中删除所有结尾字符。这意味着它将删除字符串右侧的所有指定字符。
如果无涯教程不指定参数，它将从字符串中删除所有空格。此方法返回一个字符串值。'''

# rstrip - 语法
# rstrip([chars])
# rstrip - 参数
# chars：要从字符串中删除的字符。
#
# rstrip - 返回
# 它返回字符串。



# 一个简单的示例，不带任何参数。它从字符串中删除所有结尾的空格。

# Python rstrip() method example
# 变量声明
str1 = "Java and C# "
# 调用函数
str2 = str.rstrip()
# 显示结果
print("Old string: ", str1)
print("New String: ", str2)

# 输出：
#
# Old
# string: Java and C  #
# New
# String: Java and C  #


# 根据char类型参数删除字符串char。删除字符后返回字符串。


# Python rstrip() method example
# 变量声明
str1 = "Java and C#"
# 调用函数
str2 = str.rstrip(  # )
# 显示结果
print("Old string: ", str1)
print("New String: ", str2)
# 输出：

# Old
# string: Java and C  #
# New
# String: Java and C


# 很容易知道通过获取字符串长度可以删除多少个字符。参见示例。显示字符串长度和字符串值。

# Python rstrip() method example

# 变量声明

str1 = "Java and C#"
# 调用函数
str2 = str1.rstrip(  # )
# 显示结果
print("Old string: ", str, len(str1))
print("New String: ", str2, len(str2))
# 输出：

# Old
# string: Java and C  # 11
# New
# String: Java and C
# 10
