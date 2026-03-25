A, B, S, T = map(int, input().split())

ans = 0
for i in range(1, A + 1):
  for j in range(1, B + 1):
    if i % j >= S and i % j <= T:
      ans = ans + 1

print(ans)