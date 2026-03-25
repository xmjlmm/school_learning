'''
2.设计一个程序，反映病人到医院看病、排队看医生的情况。
    要求：采用链队列存储结构。
'''

class Node(object):
    def __init__(self):
        self.data = None
        self.point = None

class LinkQueue(object):
    def __init__(self):
        self.head = None

    def queue_is_empty(self):
        return self.head is None

    def queue_push(self, elem):
        node = Node()
        node.data = elem
        if self.queue_is_empty():
            self.head = node
        else:
            cur = self.head
            while cur.point:
                cur = cur.point
            cur.point = node
        return

    def queue_pop(self):
        if self.queue_is_empty():
            print('没有人排队,请先挂号')
            return
        front_node = self.head
        cur_patient = front_node.data
        front_node.data = None
        self.head = self.head.point
        return cur_patient

def main():
    queue = LinkQueue()
    while True:
        print('1.挂号   2.看医生   3.就诊完毕   4.退出')
        choice = input('请输入你的选择:')
        if choice == '1':
            name = input('请输入你的姓名:')
            queue.queue_push(name)
            print('挂号成功')
        elif choice == '2':
            if queue.queue_is_empty():
                print('没有人在排队')
                continue
            patient = queue.queue_pop()
            print('请{},到诊室就诊'.format(patient))
        elif choice == '3':
            print('就诊完毕')
        elif choice == '4':
            break
        else:
            print('输入有误,请重新输入')

if __name__ == '__main__':
    main()