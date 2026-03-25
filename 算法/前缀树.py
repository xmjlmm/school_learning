class TrieNode:
    def __init__(self):
        self.children = {}   # 子节点的字典，键为字符，值为节点对象
        self.is_end = False  # 是否是一个单词的结束节点
        self.pass_count = 0  # 统计每个字符访问的次数
        self.end_count = 0   # 统计关键词访问的次数

class Trie:
    def __init__(self):
        self.root = TrieNode()  # 初始化根节点

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # 如果字符不在子节点中，则创建新的节点
            node = node.children[char]  # 移动到下一个节点
            node.pass_count += 1  # 更新字符访问次数
        node.is_end = True  # 标记当前节点为单词结束节点
        node.end_count += 1  # 更新关键词访问次数

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False  # 如果字符不在子节点中，返回False
            node = node.children[char]  # 移动到下一个节点
        return node.is_end  # 返回当前节点是否为单词结束节点

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False  # 如果字符不在子节点中，返回False
            node = node.children[char]  # 移动到下一个节点
        return True  # 返回以该前缀开头的单词是否存在

    def delete(self, word):
        if not self.search(word):
            return False  # 如果单词不存在，直接返回 False
        nodes_to_remove = []  # 用于保存需要删除的节点
        node = self.root
        for char in word:
            child_node = node.children[char]
            child_node.pass_count -= 1  # 减少字符访问次数
            if child_node.pass_count == 0:
                nodes_to_remove.append((node, char))  # 将需要删除的节点加入列表
            node = child_node

        # 删除到单词末尾，更新单词结束节点
        node.is_end = False
        node.end_count -= 1

        # 逐级删除不再需要的节点
        for parent, char in reversed(nodes_to_remove):
            del parent.children[char]

        return True  # 单词删除成功

def main():
    trie = Trie()
    words = ["apple", "banana", "orange", "app"]
    for word in words:
        trie.insert(word)

    print(trie.search("apple"))    # True
    print(trie.search("app"))      # True
    print(trie.search("banana"))   # True
    print(trie.search("orange"))   # True
    print(trie.search("grape"))    # False
    print('-------------------------------')
    print(trie.starts_with("app"))  # True
    print(trie.starts_with("ban"))  # True
    print(trie.starts_with("ora"))  # True
    print(trie.starts_with("gr"))   # False
    print('--------------------------------')
    print(trie.delete("apple"))   # True
    print(trie.delete("graph"))   # False

if __name__ == "__main__":
    main()
