'''2. 给定关键字序列为{16,5,17,29,11,3,15,20}，
按表中元素的顺序依次插入，建立相应的二叉排序树，给出其中序序列。'''

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return TreeNode(key)
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    return root

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)

def main():
    keys = [16, 5, 17, 29, 11, 3, 15, 20]
    root = None
    for key in keys:
        root = insert(root, key)
    print("中序序列:")
    inorder_traversal(root)

if __name__ == "__main__":
    main()


