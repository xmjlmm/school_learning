'''2.回文指的是一个字符串从前面读和从后面读都一样，编写一个算法判断一个字符串是否为回文。
要求：
1）采用链栈实现算法；
2）从键盘输入一个字符串，输出判断结果。'''

class Node(object):
    def __init__(self, elem):
        self.elem = elem
        self.point = None

class LinkList(object):
    def __init__(self):
        self.head = None

    def add(self, ele):
        node = Node(ele)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.point is not None:
                cur = cur.point
            cur.point = node

    # 快慢指针找到链表中间的元素
    def mid(self):
        # 快慢指针初始化定义
        p, q = self.head, self.head
        count = 0
        while q and q.point:
            p, q = p.point, q.point.point
        return p

    # 对后半部分链表进行反转
    def rev(self, cur):
        prev = None
        while cur:
            next_node = cur.point
            cur.point = prev
            prev = cur
            cur = next_node
        return prev

    def match(self, p):
        cur_l = self.head
        while cur_l.point is not None:
            if p.elem != cur_l.elem:
                return False
            p, cur_l = p.point, cur_l.point
        return True

if __name__ == '__main__':
    s = input('请输入一个字符串：')
    link = LinkList()
    for i in s:
        link.add(i)
    p = link.rev(link.mid())
    if link.match(p):
        print('{}是回文数'.format(s))
    else:
        print('{}不是回文数'.format(s))















