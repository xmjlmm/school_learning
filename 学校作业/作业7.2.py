'''2.假设二叉树采用二叉链存储结构，编写一个算法，
求出二叉树中的最大结点值。并设计主函数调用上述算法。'''

class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class LinkedBinaryTree(object):
    def __init__(self, root=None):
        self.root = root

    def find_max(self, node):
        if node is None:
            return float('-inf')
        return max(node.value, self.find_max(node.left), self.find_max(node.right))

    def get_max(self):
        return self.find_max(self.root)

def main():
    # 构造二叉树
    #       1
    #      / \
    #     2   3
    #    / \   \
    #   4   5   6
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(6)
    tree = LinkedBinaryTree(root)
    print("最大结点值:", tree.get_max())

if __name__ == "__main__":
    main()
