'''
isdigit：是否为数字字符，
包括Unicode数字，单字节数字，双字节全角数字，
不包括汉字数字，罗马数字、小数
'''


def isnumber(s):
    print(s+' isdigit: ',s.isdigit())
    print(s+' isdecimal: ',s.isdecimal())
    print(s+' isnumeric: ',s.isnumeric())

def main():
    isnumber('123')
    isnumber('123.0')
    isnumber('壹贰叁')
main()