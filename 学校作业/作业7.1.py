# '''1.设计一个程序，由给定的二叉树顺序存储结构建立其二叉链存储结构，
# 并利用遍历算法，求出二叉树的先序序列、中序序列和后序序列。'''
# class TreeNode(object):
#     def __init__(self, node, left=None, right=None):
#         self.node = node
#         self.left = left
#         self.right = right
#
#     def create_binary_tree(sequence):
#         if not sequence:
#             return None
#         root = TreeNode(sequence[0])
#         length = len(sequence)
#         queue = [root]
#         i = 1
#         while i < length:
#             node = queue.pop(0)
#             if i < length:
#                 node.left = TreeNode(sequence[i]) if sequence[i] is not None else None
#                 if node.left:
#                     queue.append(node.left)
#                 i += 1
#             if i < length:
#                 node.right = TreeNode(sequence[i]) if sequence[i] is not None else None
#                 if node.right:
#                     queue.append(node.right)
#                 i += 1
#         return root
#
class Traversal(object):
    def __init__(self, root):
        self.root = root

    def preorder_traversal(self, node):
        if not node:
            return
        print(node.node, end=' ')
        self.preorder_traversal(node.left)
        self.preorder_traversal(node.right)

    def inorder_traversal(self, node):
        if not node:
            return
        self.inorder_traversal(node.left)
        print(node.node, end=' ')
        self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        if not node:
            return
        self.postorder_traversal(node.left)
        self.postorder_traversal(node.right)
        print(node.node, end=' ')

def main():
    sequence = [1, 2, 3, 4, 5, 6, 7]
    root = TreeNode.create_binary_tree(sequence)
    traversal = Traversal(root)
    print("先序遍历:")
    traversal.preorder_traversal(traversal.root)
    print("\n中序遍历:")
    traversal.inorder_traversal(traversal.root)
    print("\n后序遍历:")
    traversal.postorder_traversal(traversal.root)

if __name__ == "__main__":
    main()


# # 创建一个 TreeNode 类，表示二叉树的节点
# class TreeNode:
#     def __init__(self, val):
#         self.val = val
#         self.left = None
#         self.right = None
#
#
# # 创建一个 pre_travel 函数，用于先序遍历
# def pre_travel(root):
#     result = []
#
#     def traverse(node):
#         if node:
#             result.append(node.val)
#             traverse(node.left)
#             traverse(node.right)
#
#     traverse(root)
#     return result
#
#
# # 创建一个mid_travel函数，用于中序遍历
# def mid_travel(root):
#     result = []
#
#     def traverse(node):
#         if node:
#             traverse(node.left)
#             result.append(node.val)
#             traverse(node.right)
#
#     traverse(root)
#     return result
#
#
# # 创建一个after_travel函数，用于后序遍历
# def after_travel(root):
#     result = []
#
#     def traverse(node):
#         if node:
#             traverse(node.left)
#             traverse(node.right)
#             result.append(node.val)
#
#     traverse(root)
#     return result


# 主函数
if __name__ == "__main__":
    # 构造二叉树
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    # 调用先序遍历算法
    pre_seq = pre_travel(root)
    mid_seq = mid_travel(root)
    after_seq = after_travel(root)
    print("二叉树的先序遍历序列为:", pre_seq)
    print("二叉树的中序遍历序列为:", mid_seq)
    print("二叉树的后序遍历序列为:", after_seq)
