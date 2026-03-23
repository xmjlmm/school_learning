#嵌套if
#嵌套if
   #语法结构：if条件表达式
          #if内层条件表达式
             #内存条件执行体1
          #else:
             #内存条件执行体2
    #else:
      #条件执行体
'''会员  >=200  8折
         >=100  9折
                不打折
    非会员  >=200  9.5折
                 不打折'''
answer=(input('您是会员吗？y/n'))
money=float(input('请输入您的购物金额：'))
#外层判断是否是会员
if answer=='y':  #会员
    print('会员')
    if money>=200:
        print('打8折，付款金额为:',money*0.8)
    elif 100<=money<200:
        print('打9折，付款金额为:',money*0.9)
    else:
        print('不打折，付款金额为:',money)
else:            #非会员
    print('非会员')
    if money>=200:
        print('打9.5折，付款金额为：',money*0.95)
    else:
        print('不打折，付款金额为：',money)

