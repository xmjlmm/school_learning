import math
st =input('')
ls = st.split(' ')
length = len(ls)
lp = 0
min_lp = math.inf
for i in range(length):
    ele = ls[i]
    sum = 0
    for j in ele:
        sum = sum + int(j)
    if sum < min_lp:
        min_lp = sum
        lp = i
print(min_lp,lp)
