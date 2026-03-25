
def f(n, a, visit, length, result):
    if n == length:
        result.append(visit[:])  # 收集当前的组合
        return
    for i in a:
        if i not in visit:
            visit.append(i)
            f(n + 1, a, visit, length, result)  # 递归
            visit.remove(i)

def main():
    a = [3,5,1,4]
    visited = []
    length = len(a)
    result = []  # 用来保存所有的组合结果
    f(0, a, visited, length, result)
    print(result)

main()



# def f(n, a, visit, length):
#     if n == length:
#         return [visit]  # 返回当前结果
#     result = []  # 用来保存递归过程中产生的所有结果
#     for i in a:
#         if i not in visit:
#             visit_copy = visit.copy()  # 创建visit的副本
#             visit_copy.append(i)
#             result.extend(f(n+1, a, visit_copy, length))  # 传递副本并扩展结果列表
#     return result  # 返回所有结果
#
# def main():
#     a = 'abc'
#     visited = []
#     length = len(a)
#     ans = f(0, a, visited, length)
#     print(ans)
#
# main()
