'''
1.已知有两个按元素值递增有序的顺序表A和B
设计一个算法将表A和表B的全部元素归并为一个按元素值递增有序的顺序表C
从键盘输入顺序表A和B的各元素，编程实现上述算法，
输出顺序表A、顺序表B和顺序表C 的所有元素值 。
'''

def error(A, B):
    if A.sort() != A and B.sort() != B:
        return False
    return True

def main():
    A = list(map(int, input('请输入顺序表A(每个元素之间用空格隔开):').split()))
    B = list(map(int, input('请输入顺序表B(每个元素之间用空格隔开):').split()))
    lengthA, lengthB = len(A), len(B)
    print('列表A:', A)
    print('列表B:', B)
    # 需要辅助空间
    C = []
    # 初始化两个列表的指针
    i, j = 0, 0
    while i < lengthA and j < lengthB:
        if A[i] < B[j]:
            C.append(A[i])
            i += 1
        else:
            C.append(B[j])
            j += 1
    if i == lengthA:
        C.extend(B[j:])
    if j == lengthB:
        C.extend(A[i:])
    print('列表C:', C)

if __name__ == '__main__':
    '''
    需要辅助空间O(len(A)+len(B))
    时间复杂度O(len(A)+len(B))
    '''
    main()



