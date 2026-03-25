'''ans = []
for n in range(10000000, 100000000000000000):
    if n % 2 == 1 and n % 3 == 2 and n % 4 == 1 and n % 5 == 4 and n % 6 == 5 and n % 7 == 4 and n % 8 == 1 and n % 9 == 2 and n % 10 == 9 and n % 11 == 0 and n % 12 == 5 and n % 13 == 10 and n % 14 == 11 and n % 15 == 14 and n % 16 == 9 and n % 17 == 0 and n % 18 == 11 and n % 19 == 18 and n % 20 == 9 and n % 21 == 11 and n % 22 == 11 and n % 23 == 15 and n % 24 == 17 and n % 25 == 9 and n % 26 == 23 and n % 27 == 20 and n % 28 == 25 and n % 29 == 16 and n % 30 == 29 and n % 31 == 27 and n % 32 == 25 and n % 33 == 11 and n % 34 == 17 and n% 35 == 4 and n % 36 == 29 and n % 37 == 22 and n % 38 == 37 and n % 39 == 23 and n % 40 == 9 and n % 41 == 1 and n % 42 == 11 and n % 43 == 11 and n % 44 == 33 and n % 45 == 29 and n % 46 == 15 and n % 47 == 5 and n % 48 == 41 and n % 49 == 46:
        ans.append(n)
print(ans)'''


a = []
for i in range(2, 50):
    a.append(i)

num = [1,2,1,4,5,4,1,2,9,0,5,10,11,14,9,0,11,18,9,11,11,15,17,9,23,20,25,16,29,27,25,11,17,4,29,22,37,23,9,1,11,11,33,29,15,5,41,46]
length = len(num)

ans = []
for n in range(999999999999999, 1000010000000000, 22):
    for j in range(length):
        if n % a[j] == num[j]:
            continue
        else:
            break
    if j == length - 1:
        ans.append(n)
    # if n % 2 == 1 and n % 3 == 2 and n % 4 == 1 and n % 5 == 4 and n % 6 == 5 and n % 7 == 4 and n % 8 == 1 and n % 9 == 2 and n % 10 == 9 and n % 11 == 0 and n % 12 == 5 and n % 13 == 10 and n % 14 == 11 and n % 15 == 14 and n % 16 == 9 and n % 17 == 0 and n % 18 == 11 and n % 19 == 18 and n % 20 == 9 and n % 21 == 11 and n % 22 == 11 and n % 23 == 15 and n % 24 == 17 and n % 25 == 9 and n % 26 == 23 and n % 27 == 20 and n % 28 == 25 and n % 29 == 16 and n % 30 == 29 and n % 31 == 27 and n % 32 == 25 and n % 33 == 11 and n % 34 == 17 and n% 35 == 4 and n % 36 == 29 and n % 37 == 22 and n % 38 == 37 and n % 39 == 23 and n % 40 == 9 and n % 41 == 1 and n % 42 == 11 and n % 43 == 11 and n % 44 == 33 and n % 45 == 29 and n % 46 == 15 and n % 47 == 5 and n % 48 == 41 and n % 49 == 46:
        # ans.append(n)
print(ans)