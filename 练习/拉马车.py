import os
import sys

# 请在此输入您的代码


a = input()
a = list(a)
b = input()
b = list(b)
queue = []
# 队列 先进先出
length_a, length_b = len(a), len(b)
# turn = 0 A, 1 B
turn = 0
# 1. tmp 不存在在queue
while length_a != 0 and length_b != 0:
  length_a, length_b = len(a), len(b)
  print('queue',queue)
  print('a',a)
  print('b',b)
  if turn == 0 and length_a != 0:
    tmp = a.pop(0)
    if tmp not in queue:
      queue.append(tmp)
      turn = 1
    else:
      for j in range(len(queue)):
        if tmp == queue[j]:
          break
      print('queue', queue, 'j', j, 'tmp', tmp)
      for k in range(j, len(queue)):
        cc = queue.pop(j)
        a.append(cc)
      a.append(tmp)
  if length_b != 0 and turn == 1:
    print('b', b)
    tmp = b.pop(0)
    if tmp not in queue:
      queue.append(tmp)
      turn = 0
    else:
      for j in range(len(queue)):
        if tmp == queue[j]:
          break
      for k in range(j, len(queue)):
        cc = queue.pop(j)
        b.append(cc)
      b.append(tmp)

if length_b == 0:
  print(a)
else:
  print(b)
