n = int(input())
list_input = list(map(int, input().split()))

max_index = []
min_index = []
max_num = -math.inf
min_num = math.inf
for num in list_input:
    if num > max_num:
        max_num = num
    if num < min_num:
        min_num = num
# print(max_num, min_num)
for index in range(n):
    if list_input[index] == max_num:
        max_index.append(index)
    if list_input[index] == min_num:
        min_index.append(index)
# print(max_index, min_index)
min_length = n + 1
i, j = 0, 0
# max_length = len(max_index)
# min_length = len(min_index)

# for i in range(max_length):
#     for j in range(min_length):
#         length_possible = abs(max_index[i] - min_index[j]) + 1
#         if length_possible <= min_length:
#             min_length = length_possible
for i in max_index:
    for j in min_index:
        min_length = min(min_length, abs(i - j) + 1)


print(min_length)
