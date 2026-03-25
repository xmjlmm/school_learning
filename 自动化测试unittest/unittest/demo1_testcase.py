import unittest

# 假设功能函数counter的定义
def counter(a, b, method):
    if method == '+':
        return a + b
    elif method == '-':
        return a - b
    else:
        raise ValueError("Unsupported method")

class TestDemo1(unittest.TestCase):
    def test_01add(self):
        # 准备用例数据
        params = {'a': 11, 'b': 22, 'method': '+'}
        expected = 33
        # 调用功能函数，获取实际结果
        result = counter(**params)
        # 比对预期结果和实际结果是否一致（断言）
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
