import string

def english_text_tokenize(text):
    """
    英文文本分词函数
    :param text: 输入的英文文本字符串
    :return: 分词后的列表
    """
    # 定义所有标点符号
    punctuations = string.punctuation
    # 初始化一个空列表用于存储分词结果
    tokens = []
    # 对文本按空格进行初步拆分
    words = text.split()
    for word in words:
        # 去除单词两端的标点符号
        word = word.strip(punctuations)
        if word:
            tokens.append(word)
    return tokens

# 测试示例
text = input('请输入英文文本：')
result = english_text_tokenize(text)
print(result)