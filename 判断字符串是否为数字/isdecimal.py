'''isdecimal：是否为十进制数字符，
包括Unicode数字、双字节全角数字，
不包括罗马数字、汉字数字、小数；'''


def isnumber(s):
    print(s+' isdigit: ',s.isdigit())
    print(s+' isdecimal: ',s.isdecimal())
    print(s+' isnumeric: ',s.isnumeric())


isnumber('123')
isnumber('123.0')
isnumber('壹贰叁')





