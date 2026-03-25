'''1.建立一个单链表，并设计一个算法,通过一趟遍历确定单链表中元素值最大的结点。
要求：
单链表的数据为8个整数，从键盘输入。'''
import os
import sys
import math
# 定义一个链表节点
class Node(object):
    def __init__(self, elem):
        self.elem = elem
        self.next = None
# 创建一个单链表
class Linklist(object):
    # 初始化头指针
    def __init__(self):
        self.head = None
    # 判断链表是否为空
    def is_empty(self):
        return self.head == None
    # 计算链表的长度
    def length(self):
        cur = self.head
        count = 0
        while cur.next is not None:
            count += 1
            cur = cur.next
        return count
    # 在链表中添加元素
    def add(self, elem):
        node = Node(elem)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
    # 遍历列表，找到列表中最大的那个元素
    def travel_max(self):
        cur = self.head
        max = -math.inf
        while cur.next is not None:
            cur = cur.next
            if cur.elem > max:
                max = cur.elem
        return max
# 程序调试
if __name__ == '__main__':
    ls = Linklist()
    set_number = 8
    for i in range(set_number):
        elem = int(input(''))
        ls.add(elem)
    print('the max elem is {}'.format(ls.travel_max()))




























