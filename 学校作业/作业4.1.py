'''
1.设从键盘输入一整数序列a1,a2,…,an，
试编程实现：当ai<0时，ai进队；当ai>0时，将队首元素出队；
当ai=0时，表示输入结束。
最后输出队列中的所有元素。
要求：
1）采用环形队列存储结构；
2）有异常处理功能。
'''

class CircularQueue(object):
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.max_size = 10
        self.queue = [None] * self.max_size

    def queue_is_empty(self):
        return self.front == self.rear

    def queue_is_full(self):
        return (self.rear + 1) % self.max_size == self.front

    def queue_push(self, data):
        if self.queue_is_full():
            print("Queue is full!")
            return False
        self.queue[self.rear] = data
        self.rear = (self.rear + 1) % self.max_size
        return True

    def queue_pop(self):
        if self.queue_is_empty():
            print("Queue is empty!")
            return None
        data = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.max_size
        return data

    def queue_show(self):
        if self.queue_is_empty():
            print('Queue is empty!')
            return
        index_cur = self.front
        while index_cur != self.rear:
            print(self.queue[index_cur], end=' ')
            index_cur = (index_cur + 1) % self.max_size
        print()
        return

def main():
    queue = CircularQueue()
    LinkList = input('请输入整数序列，以逗号分隔：')
    try:
        LinkList = [int(x) for x in LinkList.split(',')]
    except ValueError:
        print('输入错误，请输入整数序列！')
        return
    for data in LinkList:
        if data < 0:
            if not queue.queue_is_full():  # 在这里检查队列是否已满
                queue.queue_push(data)
            else:
                print("操作无法继续：队列已满。")
        elif data > 0:
            if not queue.queue_is_empty():  # 在这里检查队列是否为空
                queue.queue_pop()
            else:
                print("操作无法继续：队列已空。")
        elif data == 0:
            break
        queue.queue_show()

if __name__ == '__main__':
    main()