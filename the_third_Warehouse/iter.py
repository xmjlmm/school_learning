from collections.abc import Iterable


class MyList(object):
	def __init__(self):
		self.container = []
	def __iter__(self):  # 只要有此方法最下面的结果就是True
		pass

	def add(self, item):
		self.container.append(item)


myList = MyList()
myList.add(11)
myList.add(22)
myList.add(33)

print(isinstance(myList, Iterable))  # 如果结果是True 则表示mylist一定是可迭代对象，否则是不可迭代对象


from collections.abc import Iterable
from collections.abc import Iterator

class MyList(object):
	'''自定义的一个可迭代对象'''
	def __init__(self):
		self.items = []

	def add(self, val):
		self.items.append(val)

	def __iter__(self):
		# 这个方法有两个功能
		# 1.标记用当前类创建出来的对象一定是 可迭代对象
		# 2.当调用iter()函数的时候 这个方法会被自动调用 它返回自己指定的哪个迭代器
		return MyIterator()

class MyIterator(object):
	'''自定义的供上面可迭代对象使用的一个迭代器'''
	def __init__(self):
		pass

	def __next__(self):
		# 这个方法有两个功能
		# 1.标记当前类创建出来的对象（当然还必须有__iter__方法）一定是迭代器
		# 2.当调用next()函数的时候 这个方法会被自动调用 它返回一个数据
		pass

	def __iter__(self):
		pass

mylist = MyList()	# 可迭代对象
mylist_iter = iter(mylist)	# 当对mylist调用iter()函数的时候，会自动调用MyList类中的__iter__方法，返回的就是mylist这个可迭代对象的迭代器

print("mylist是否是可迭代对象", isinstance(mylist, Iterable))	# True
print("mylist是否是迭代器", isinstance(mylist, Iterator))	# False

print("mylist_iter是否是可迭代对象", isinstance(mylist_iter, Iterable))	# True
print("mylist_iter是否是迭代器", isinstance(mylist_iter, Iterator))	# True

# next(mylist_iter)


from collections.abc import Iterable
from collections.abc import Iterator


class MyList(object):
	'''自定义的一个可迭代对象'''
	def __init__(self):
		self.items = []
		self.current = 0

	def add(self, val):
		self.items.append(val)

	def __iter__(self):
		return self

	def __next__(self):
		if self.current < len(self.items):
			item = self.items[self.current]
			self.current += 1
			return item
		else:
			raise StopIteration  # 抛出异常（不返回None是因为，for循环是一个已实现的功能，它自带iter、next函数，并且带有异常判断，通过这个异常判断来决定是否还需要继续获取迭代器的数据，如果用None来表示数据已获取完毕，但是for循环的代码依然用的异常来判断而不是None，所以for循环会产生死循环）


if __name__ == '__main__':
	mylist = MyList()
	mylist.add(1)
	mylist.add(2)
	mylist.add(3)
	mylist.add(4)
	mylist.add(5)

	# mylist_iter = iter(mylist)
	# print(next(mylist_iter))

	# for num in mylist:
	#	print(num)
	nums = list(mylist)  # list在创建一个新的列表的时候，只要是 可迭代对象 就可以放到list中当作实参
	print(nums)


