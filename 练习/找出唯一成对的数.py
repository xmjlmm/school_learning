''' 法1
ls = []
for i in range(1,1001):
    ls.append(i)

# nums是1001个数的数组
for ele in nums:
    if ele in ls:
        ls.remove(ele)
    else:
        print(ele)
        break
'''

'''法2
nums.sort()
for i in range(len(nums) - 1):
    if nums[i] == nums[i+1]:
        print(nums[i])
        break
'''

'''法3
res = 0
for i in range(1, 1001):
    res = res ^ i
    
for i in range(len(nums)):
    res = res ^ nums[i]
print(res)


'''