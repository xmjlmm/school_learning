#多分支结构
#多分支结构
      #中文语义：成绩是在90分以上吗？不是
              #成绩是在80分到90分之间吗？不是
              #成绩是在70分到80分之间吗？不是
              #成绩是在60分到70分之间吗？不是
              #成绩是在60分以下吗？是
      #语法结构：if条件表达式1：条件执行体1
      #elif条件表达式2：条件执行体2
      #elif表达表达式N：条件执行体N
      #else:条件执行体N+1
'''多分支结构，多选一执行
从键盘录入一个整数 成绩
90-100 A
80-89  B
70-79  C
60-69  D
0-59   E
小于0或大于100 为非法数据（不是成绩地有效范围）
'''
score=int(input('请输入一个成绩：'))
if score>=90 and score<=100:
    print('A级')
elif score>=80 and score<=89:
    print('B级')
elif score>=70 and score<=79:
    print('C级')
elif score>=60 and score<=69:
    print('D级')
elif score>=0 and score<=59:
    print('E级')
else:
    print('对不起，成绩有误，不在成绩地有效范围')
# 90<=score<=100  （可以）

