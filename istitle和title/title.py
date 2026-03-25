'''
title() 方法：
title() 方法用于将字符串中的每个单词的首字母转换为大写字母，
同时将其余字母转换为小写字母。
它将字符串转换为标题文本格式。
'''

text = "this is a title"
formatted_text = text.title()
print(formatted_text)  # 输出结果为 "This Is A Title"



text2 = "THIS IS A title"
formatted_text2 = text2.title()
print(formatted_text2.istitle())


