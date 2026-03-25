# 1:导包
import unittest
import unittest.mock

# 2: 创建模拟的类
class MyTest(unittest.TestCase):
    def hello(self):
        print('hello')

    def test_return(self):
        # 创建一个能返回250的可调用对象
        mock_obj = unittest.mock.Mock(return_value = self.hello())
        # 调用mocke对象，拿到返回值
        ret = mock_obj()
        print(ret)

if __name__ == '__main__':
    unittest.main()