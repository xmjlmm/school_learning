class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.lchild = None
        self.rchild = None

def pre_order(root, ans):
    if root:
        ans.append(root.data)
        # print(root.data)
        pre_order(root.lchild, ans)
        pre_order(root.rchild, ans)
    return ans

def in_order(root, ans):
    if root:
        in_order(root.lchild, ans)
        ans.append(root.data)
        in_order(root.rchild, ans)
    return ans

def post_order(root, ans):
    if root:
        post_order(root.lchild, ans)
        post_order(root.rchild, ans)
        ans.append(root.data)
    return ans

a = BiTreeNode("A")
b = BiTreeNode("B")
c = BiTreeNode("C")
d = BiTreeNode("D")
e = BiTreeNode("E")
f = BiTreeNode("F")
g = BiTreeNode("G")

e.lchild = a
e.rchild = g
a.rchild = c
c.lchild = b
a.lchild = d
c.rchild = f
root = e

print(root.data)

ans = []
print(pre_order(root, ans))

ans = []
print(in_order(root, ans))

ans = []
print(post_order(root, ans))

