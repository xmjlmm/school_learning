class Node:
    def __init__(self, name, type="dir"):
        self.name = name
        self.type = type
        self.children = []
        self.parent = None
    def get_parent(self):
        return self.parent

n = Node("hello")
nn = Node("world")
n.children.append(n2)
n.parent = nn.name
print(n.get_parent())
nn.parent = n
parent_node = nn.get_parent()
print(parent_node.name)
print(nn.get_parent())

n1 = Node('hello', 'dir')
n2 = Node('World', 'dir')
n1.parent = n2
n2.children.append(n1)
print(n1.get_parent().name)