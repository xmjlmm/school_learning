list1 = [1,2,3,3,4,5,6,6]
ans = list1.count(3)
print(ans)

# 1
list1 = ['hello', 'world', 'hello', 'python', 'hello']
sub_str = 'hello'
sum = 0
for i in list1:
    if sub_str in i:
         sum += 1
print(sum)



# 2
list1 = [1,2,3,3,4,5,6,6]
dict1 = {}
for i in list1:
    dict1[i] = list1.count(i)
print(dict1)

