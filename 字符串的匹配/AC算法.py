'''
使用ac算法对字符串进行匹配
时间复a杂度O（n）
最快的线性时间复杂度
'''

class TrieNode:
    def __init__(self):
        self.children = {}   # 子节点的字典，键为字符，值为节点对象
        self.fail = None     # 失败指针，指向失败时应该跳转到的节点
        self.is_end = False  # 是否是一个单词的结束节点
        self.length = 0      # 当节点是单词结束节点时，记录该单词的长度

class ACAlgorithm:
    def __init__(self):
        self.root = TrieNode()  # 初始化根节点

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # 如果字符不在子节点中，则创建新的节点
            node = node.children[char]  # 移动到下一个节点
        node.is_end = True  # 标记当前节点为单词结束节点
        node.length = len(word)  # 记录单词长度

    def build_fail(self):
        queue = []
        self.root.fail = None
        queue.append(self.root)
        while queue:
            current_node = queue.pop(0)
            for char, child_node in current_node.children.items():
                if current_node == self.root:
                    child_node.fail = self.root
                else:
                    fail_node = current_node.fail
                    while fail_node:
                        if char in fail_node.children:
                            child_node.fail = fail_node.children[char]  # 设置失败指针
                            break
                        fail_node = fail_node.fail
                    if not fail_node:
                        child_node.fail = self.root
                queue.append(child_node)

    def search(self, text):
        current_node = self.root
        for i, char in enumerate(text):
            while char not in current_node.children and current_node != self.root:
                current_node = current_node.fail  # 失败时跳转到失败指针指向的节点
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                current_node = self.root
            temp_node = current_node
            while temp_node:
                if temp_node.is_end:
                    print("在位置 {} 匹配到字符串".format(i - temp_node.length + 1))  # 打印匹配结果
                temp_node = temp_node.fail

def main():
    ac = ACAlgorithm()
    keywords = ["关键词", "算法", "示例"]
    text = "这是一个示例，用于演示关键词匹配算法的示例实现。"
    for word in keywords:
        ac.insert(word)
    ac.build_fail()
    ac.search(text)

# 示例
if __name__ == "__main__":
    main()

