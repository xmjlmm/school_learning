import re
import sys
def tokenize(text):
    pattern = r"\w+(?:'\w+)?|\d*\.\d+|\w+"
    return [token for token in re.findall(pattern,text) if token.strip()]

text = input("请输入英文文本:")
print("分词结果:",tokenize(text))
