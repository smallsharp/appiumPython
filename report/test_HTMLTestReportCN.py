# -*- coding:utf-8 -*-

import unittest
from report import HTMLTestReportCN


# 测试用例

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        self.assertEqual(2, 2, "testError")

    def testCase2(self):
        self.assertEqual(2, 3, "testError")

    def testCase3(self):
        self.assertEqual(2, 5, "测试错误")

    def testCase4(self):
        self.assertEqual(2, 1, "测试错误")

    def testCase5(self):
        pass


class APITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        self.assertEqual(2, 2, "testError")

    def testCase2(self):
        self.assertEqual(3, 3, "testError")

    def testCase3(self):
        self.assertEqual(5, 5, "testError")

    def testCase4(self):
        self.assertEqual(2, 1, "测试错误")

    def testCase5(self):
        self.assertEqual(2, 9, "testError")

    def testCase6(self):
        pass


# 添加Suite
def Suite():
    # 定义一个单元测试容器
    suiteTest = unittest.TestSuite()
    # 将测试用例加入到容器
    suiteTest.addTest(MyTestCase("testCase1"))
    suiteTest.addTest(MyTestCase("testCase2"))
    suiteTest.addTest(MyTestCase("testCase3"))
    suiteTest.addTest(MyTestCase("testCase4"))
    suiteTest.addTest(MyTestCase("testCase5"))
    suiteTest.addTest(APITestCase("testCase1"))
    suiteTest.addTest(APITestCase("testCase2"))
    suiteTest.addTest(APITestCase("testCase3"))
    suiteTest.addTest(APITestCase("testCase4"))
    suiteTest.addTest(APITestCase("testCase5"))
    suiteTest.addTest(APITestCase("testCase6"))
    return suiteTest


'''
run in console
'''
if __name__ == '__main__':
    # 确定生成报告的路径
    filePath = r'E:\HTMLTestReportCN1212.html'
    fp = open(filePath, 'wb')
    # 生成报告的Title,描述
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fp,
        title='自动化测试报告',
        # description='详细测试用例结果',
        tester='lee'
    )
    # 运行测试用例
    runner.run(Suite())
    # 关闭文件，否则会无法生成文件
    fp.close()
