def binary_enum(list, n):
    result = []
    total = 2 ** n
    for i in range(total):
        subset = []
        for j in range(n):
            # 检查二进制数i的第j位是否为1。如果是，表示集合中的第j + 1个元素被选择。
            if i & (1 << j):
                subset.append(list[j])  # 因为列表索引从0开始，所以加1以表示元素编号
        result.append(subset)
    return result

# 示例：生成集合 {1, 2, 3} 的所有子集
list = [44, 21, 43]
n = 3
subsets = binary_enum(list, n)
for subset in subsets:
    print(subset)