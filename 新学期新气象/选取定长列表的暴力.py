def get_combinations(lst, k):
    def helper(cur_combination, start_index):
        if len(cur_combination) == k:
            result.append(cur_combination[:])
            return
        for i in range(start_index, len(lst)):
            cur_combination.append(lst[i])
            helper(cur_combination, i + 1)
            cur_combination.pop()
    result = []
    helper([], 0)
    return result


# 示例使用
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
k = 5
combinations = get_combinations(lst, k)
print(combinations)










from combinations import get_combinations


def main():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k = 3
    combinations = get_combinations(lst, k)
    print(combinations)


if __name__ == "__main__":
    main()