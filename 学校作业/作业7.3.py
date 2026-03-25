'''3.假设二叉树采用二叉链存储结构，
编写一个算法，求出二叉树中的叶子结点数。
并设计主函数调用上述算法。'''


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def count_leaf_nodes(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaf_nodes(root.left) + count_leaf_nodes(root.right)

def main():
    # 构建二叉树
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    # 调用算法求解叶子节点数
    leaf_count = count_leaf_nodes(root)
    print("叶子节点数为:", leaf_count)

if __name__ == "__main__":
    main()
