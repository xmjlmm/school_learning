'''2.设计算法，根据输入的学生人数和成绩建立一个单链表，并累计成绩不及格的人数。
要求：
   		学生人数和成绩均从键盘输入。'''

# 构建一个学生和成绩节点
class Node(object):
    def __init__(self, student, score):
        self.student = student
        self.score = score
        self.next = None
# 定义一个单链表
class LinkList(object):
    def __init__(self):
        self.head = None
    # 判断列表是否为空
    def is_empty(self):
        return self.head is None
    # 添加学生名称和学生成绩
    def add(self, student, score):
        elem = Node(student, score)
        if self.is_empty():
            self.head = elem
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = elem
    # 遍历单链表,统计不及格人数
    def num_of_fail(self):
        num = 0
        cur = self.head
        while cur:
            if cur.score < 60:
                num += 1
            cur = cur.next
        return num
# 程序测试
if __name__ == '__main__':
    ls = LinkList()
    n = int(input("请输入学生人数："))
    for i in range(n):
        student = input("请输入第{}个学生的姓名：".format(i+1))
        score = int(input("请输入第{}个学生的成绩：".format(i+1)))
        ls.add(student, score)
    print("不及格人数：", ls.num_of_fail())