import unittest

from pythonProject.高级脚本.自动化测试unittest.unittest.demo1_testcase import TestDemo1
from pythonProject.高级脚本.自动化测试unittest.unittest import demo1_testcase

suite = unittest.TestSuite()
load = unittest.TestLoader()
print(suite.addTest(load.loadTestsFromTestCase(TestDemo1)))
print(suite.addTest(load.loadTestsFromModule(demo1_testcase)))
suite.addTest(load.discover('testcases'))
print(suite)
print(load)