s = "hello world,  "
print(s.rstrip(" ,"))  # 输出："hello world"




s1 = "hello world\n"
print(s1.rstrip("\n"))  # 输出："hello world"


s2 = "hello world!!!"
chars_to_remove = ["!", "?"]

# 使用列表解析来去除指定的字符集合
s2 = ''.join([c for c in s2 if c not in chars_to_remove])
print(s2)


s3 = "hello worldworld"
suffix_to_remove = "world"

if s3.endswith(suffix_to_remove):
    s3 = s3[: -len(suffix_to_remove): 1]

print(s3)  # 输出："hello world"
