import unittest
import unittest.mock
# import pay
# import pay_status

class TestPay(unittest.TestCase):
    def test_success(self):
        # 用一个mock来代替pay中的pay_way函数
        pay.pay_way = unittest.mock.Mock(return_value={"result": "success", "reason":"null"})
        # 盗用要测试的函数
        ret = pay_status.pay_way_status()
        self.assertEqual(ret, '支付成功', '支付失败')

    def test_fail(self):
        pay.pay_way = unittest.mock.Mock(return_value={"result": "fail", "reason": "余额不足"})

        ret = pay_status.pay_way_status() # 调用支付状态函数
        self.assertEqual(ret, '支付失败', '测试失败')

if __name__ == '__main__':
    unittest.main()