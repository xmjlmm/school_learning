def is_power(m, n):
    if m == 1:  # m为1时，任何数的整数次方都是1
        return True
    if m == n:  # m等于n时，m是n的1次方
        return True
    if n == 1 and m != 1:  # n为1时，除了m等于1，其他数的整数次方都不是1
        return False
    if m % n == 0:  # 如果m能整除n，继续递归判断m/n是否是n的整数次方
        return is_power(m // n, n)
    return False  # 其他情况都返回False

def main():
    m = int(input('请输入m的值为：'))
    n = int(input('请输入n的值为：'))
    print(is_power(m,n))
main()
'''
'''
def analyze_lyrics(lyrics):
    word_counts = {}  # 用于记录词语出现的次数的字典
    # 去除换行符和空格，并按照空格分割歌词为单词列表
    words = lyrics.replace('\n', ' ').split()
    # 遍历歌词中的每个单词
    for i in range(len(words)-1):
        word = words[i] + words[i+1]  # 构造两个字的词语
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    # 找到出现次数最多的词语
    max_count = max(word_counts.values())
    most_common_words = [word for word, count in word_counts.items() if count == max_count]
    return most_common_words, max_count

result = analyze_lyrics(lyrics)
print("最常出现的两个字的词语及出现的次数：")
for word in result[0]:
    print("{}: {}".format(word,result[1]))
'''
'''
def analyze_lyrics(lyrics):
    word_counts = {}
    words = lyrics.replace('\n', ' ').split()
    length = len(words) - 1
    for i in range(length):
        word = words[i] + words[i+1]
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    # 找到出现次数最多的词语
    ls = sorted(word_counts.items(), key = lambda x:x[1], reverse = False)
    most_common_words = ls[0][0]
    max_count = ls[0][1]
    return most_common_words, max_count
def main():
    result = analyze_lyrics(lyrics)
    print("最常出现的两个字的词语及出现的次数：")
    for word in result[0]:
        print("{}: {}".format(word,result[1]))
main()
'''

import jieba
def analyze_lyrics(lyrics):
    lyrics = lyrics.replace('\n', '')
    ls = jieba.lcut(lyrics,cut_all=False)
    length = len(ls) - 1
    for i in range(length,-1,-1):
        if len(ls[i]) != 2:
            del ls[i]
    length = len(ls)
    word_counts = {}
    for ele in ls:
        if ele not in word_counts:
            word_counts[ele] = 1
        else:
            word_counts[ele] += 1
    lie = sorted(word_counts.items(), key = lambda x:x[1], reverse= True)
    max_count = lie[0][1]
    i = 0
    while i <= length - 1 :
        if lie[i][1] != max_count:
            break
        i = i + 1
    lb = []
    for i in range(i):
        lb.append((lie[i][0],lie[i][1]))
    return lb
def main():
    lyrics = '''高楼是你拔地的想象 街道是你动感的面庞 长桥是你华丽的首饰 霓虹是你奇幻的时装 人海是你超凡的自信 车流是你长远的目光 
    风景是你妩媚的阴柔 艺术是你传神的宝藏 亲爱的城市 我亲爱的城市 跟我一起爱你的是琴弦般的阳光 此刻我已变成一把 guitar 融入你美好的歌唱
    亲爱的城市 我亲爱的城市 跟我一起爱你的是琴弦般的阳光 此刻我已变成一把 guitar 融入你美好的歌唱'''
    res = analyze_lyrics(lyrics)
    print(res)
main()

'''
def analyze_lyrics(lyrics):
    word_counts = {}  # 用于记录词语出现的次数的字典
    # 去除换行符和空格，并按照空格分割歌词为单词列表
    lyrics = lyrics.replace('\n', '')
    words = list(lyrics)
    # 遍历歌词中的每个单词
    for i in range(len(words)-1):
        word = words[i] + words[i+1]  # 构造两个字的词语
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    max_count = max(word_counts.values())
    most_common_words = [word for word, count in word_counts.items() if count == max_count]
    return most_common_words, max_count

result = analyze_lyrics(lyrics)
print("最常出现的两个字的词语及出现的次数：")
print(result)'''

