from itertools import pairwise

ls = [1, 2, 4]
l = pairwise(ls)
for i in l:
    print(i)