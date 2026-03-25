import unittest

class MyTest(unittest.TestCase):
    def test_1(self):
        print('这是：test1')

    def test_2(self):
        print('这是：test2')

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(MyTest('test_1'))
    suite.addTest(MyTest('test_2'))

    # 运行容器中的测试案例
    runner = unittest.TextTestRunner()
    runner.run(suite)
