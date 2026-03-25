from collections import deque

q = deque()
q3 = deque("12345")
print(q, type(q))
print(q3, type(q3))


q3.appendleft('0')
q3.append('0')
print(q3)


q4 = deque('12345', maxlen = 5)
print(q4)
q4.append('0')
print(q4)
q3.insert(2, 7)

print("q3:", q3)

a = q4.pop()
print(a)
print(q4)
q4.popleft()
print("q4:", q4)



q3.remove("2")
# q3.remove(2)
print("q3:", q3)


q6 = deque([1,2,3,4,5])
q7 = deque([1,2,3,4,5])
q6.extendleft([6,7,8])
q7.extendleft(range(6,10))

print("q6", q6)
print("q7", q7)

q6.extend([6,7,8])
q7.extend(range(6,10))

print("q6", q6)
print("q7", q7)



q8 = deque([1,2,3,4,5])
q8.append(q8.popleft())

print("q8", q8)

q8.appendleft(q8.popleft())
print("q8", q8)


q9 = deque([1,2,3,4,5])
q9.rotate(3)
print("q9", q9)