import unittest
from parameterized import parameterized


class MyTest(unittest.TestCase):
    @parameterized.expand([('renshanwen', 23), ('niumiu', 25), ('shutong', 22)])
    def test_param(self, name, age):
        self.name = name
        self.age = age
        print('name: %s, age: %s' % (self.name, self.age))


if __name__ == '__main__':
    unittest.main()
