import unittest

class MyTest(unittest.TestCase):

    def test_1(self):
        print('这是：test_1')

    def test_2(self):
        print('这是：test_2')


# defaultTestLoader.discover()方法用于查找指定目录下的所有测试模块，并自动创建测试套件。
if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('./', 'test2.py')
    # 运行测试用例
    runner = unittest.TextTestRunner()
    runner.run(suite)


