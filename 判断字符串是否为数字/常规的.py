'''
读入一个字符串str，输出字符串str中的连续最长的数字串。
输入：abcd12345ed125ss123456789
输出：123456789
'''
# 1. 不使用isnumeric()
def notuse_isnumeric(str:str) -> int:
    restrict = '1234567890'
    record_num = []
    record_str = []
    count = 0
    str_str = ''
    for word in str:
        if word not in restrict:
            record_num.append(count)
            record_str.append(str_str)
            count = 0
            str_str = ''
        else:
            count += 1
            str_str = str_str + word
    record_num.append(count)
    record_str.append(str_str)
    max_num = max(record_num)
    max_str = record_str[record_num.index(max_num)]
    return (max_str, max_num)

def main():
    str = input('请输入一个字符串：')
    print(notuse_isnumeric(str))


if __name__ == '__main__':
    main()
