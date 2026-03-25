str1 = 'What\'s your name?'
str2 = "What's your name?"

# str3 = 'What's your name?'
print(str1)
print(str2)

# print(str3)


s = 'ABCDEFGHIJKLMN'
n = len(s)
b = s[n-1]
a = s[-1]
c = s[-n]

print(a,b,c)

print(s[6:0:-2]) 

s2 = 'fagaFAFAsfa'
s4 = ''

# # >97 是小写  <97 是大写
# for i in s2:
#     if ord(i)>=97:  # 小写
#         s4 += chr(ord(i)-32)
#     else:  # 大写
#         s4 += chr(ord(i)+32)
# print(s2)
# print(s4)

# print(chr(65))

# print(ord("a"))   
# print(ord("A")) 
# print(ord("A")-ord("a"))


# print(s2.upper())
# print(s2.lower())

s2 = 'fagaFAFAsfa'
s3 = 'faffhfhfhfhf'
flag = 0   # 0表示没有出现a，1表示出现a
count = 0  # 执行多少次  
for i in s3:
    count += 1
    if 'a' == i:
        flag = 1

        print(True)
        break
if flag == 0:
    print(False)

print(count)
