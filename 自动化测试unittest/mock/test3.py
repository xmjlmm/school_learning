# # 1:导包
# import unittest
# import unittest.mock
#
# # 2: 创建模拟的类
# class MyTest(unittest.TestCase):
#     def sum_ab(self, a, b):
#         self.a = a
#         self.b = b
#         return self.a + self.b
#
#     def test_return(self):
#
#         # 创建一个能返回250的可调用对象
#         mock_obj = unittest.mock.Mock(side_effect = self.sum_ab)
#         # 调用mocke对象，拿到返回值
#         print(mock_obj(1, 2))
#
# if __name__ == '__main__':
#     unittest.main()



# 1:导包
import unittest
import unittest.mock

# 2: 创建模拟的类
class MyTest(unittest.TestCase):

    def test_return(self):
        def sum_ab(a, b):
            return a + b

        # 创建一个能返回250的可调用对象
        mock_obj = unittest.mock.Mock(side_effect = sum_ab)
        # 调用mocke对象，拿到返回值
        print(mock_obj(1, 2))

    def test_return2(self):
        mock_obj = unittest.mock.Mock(side_effect=self.test_return())
        print(mock_obj(1, 2))

if __name__ == '__main__':
    unittest.main()

