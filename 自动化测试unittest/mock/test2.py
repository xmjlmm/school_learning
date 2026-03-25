import unittest.mock

# 2: 创建模拟的类
class MyTest(unittest.TestCase):

    def test_return(self):
        # 创建一个能返回250的可调用对象
        mock_obj = unittest.mock.Mock(side_effect=[1, 2, 3])
        # 调用mocke对象，拿到返回值
        for i in range(3):
            print(mock_obj())


if __name__ == '__main__':
    unittest.main()