# 声明一个列表
nums = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]

# 参数为list数组时，是压缩数据，相当于zip()函数
iters = zip(*nums)
# 输出zip(*zipped)函数返回对象的类型
print("type of iters is %s" % type(iters))
# 因为zip(*zipped)函数返回一个zip类型对象，所以我们需要对其进行转换
# 在这里，我们将其转换为字典
print(dict(iters))


grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
grids = map(max, zip(*grid))
print(list(grids))
print(grids)