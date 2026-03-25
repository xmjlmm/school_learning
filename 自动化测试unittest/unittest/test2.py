import unittest

class testMode(unittest.TestCase):
    def test1(self):
        self.assertNotEqual(11, 22)
        # self.assertEqual(11, 22)
        self.assertTrue('None')
        # self.assertFalse('None')
        self.assertIsNone(None)
        self.assertIn('a', 'abc')  # 判断字符串中是否包含某个字符
        # self.assertNotIn('a', 'abc')

if __name__ == '__main__':
    unittest.main()