'''最大公共子串长度问题就是: 求两个串的所有子串中能够匹配上的最大长度是多少。
比如:"abcdkkk"和"baabcdadabc"， 可以找到的最长的公共子串是"abcd",所以最大公共子串长度为 4。
下面的程序是采用矩阵法进行求解的，这对串的规模不大的情况还是比较有效的解法
请分析该解法的思路，并补全划线部分缺失的代码，'''

def max_length(s1, s2):
    length1 = len(s1)
    length2 = len(s2)
    if length1 < length2:
        s1, s2 = s2, s1
        length1, length2 = length2, length1
    i, j = 0, 0
    max_len = []
    while i <= length1 and j <= length2:
        if j == length2:
            return length2
        if i == length1:
            return max(max_len)
        if s1[i] == s2[j]:
            j = j + 1
        else:
            max_len.append(j)
            j = 0
            i = i - j + 1
        i = i + 1

if __name__ == '__main__':
    s1 = input('请输入第一个字符串')
    s2 = input('请输入第二个字符串')
    ans = max_length(s1, s2)
    print(ans)