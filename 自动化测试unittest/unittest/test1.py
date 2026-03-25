import unittest

class TestDemo1(unittest.TestCase):
    def test_01add(self):
        # 第一步：准备用例数据
        params = {'a': 11, 'b': 22, 'method': '+'}
        expected = 33
        # 第二步：调用功能函数(调用接口)，获取实际结果
        result = counter(**params)
        # 第三步：比对预期结果和实际结果是否一致（断言）
        # assert expected == result
        self.assertEqual(expected, result)# 比上面的assert打印更多信息
