# 编写一个Python程序，计算给定数字的二进制表示中1的个数和二进制长度。
num = 1122

binary_one_num = num.bit_count()
binary_length = num.bit_length()

print(binary_one_num)
print(binary_length)





