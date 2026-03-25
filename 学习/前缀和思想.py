# 724. 寻找数组的中心下标

ls = list(map(int, input().split()))
total_sum = sum(ls)
left_sum = 0
flag = -1

for i, num in enumerate(ls):
    # print(left_sum, total_sum - left_sum - num)
    if left_sum == total_sum - left_sum - num:
        flag = i
        break
    left_sum += num

print(flag)