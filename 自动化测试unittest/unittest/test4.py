import unittest

class Mytest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_1(self):
        print("test_1")
        a = 1 + 1
        self.assertEqual(a, 2, '结果不为2')

    def test_2(self):
        print("test_2")
        b = 1 + 2
        self.assertNotEqual(b, 2, '结果不为2')

if __name__ == "__main__":
    unittest.main()