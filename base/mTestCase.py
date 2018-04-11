# -*- coding: utf-8 -*-
import os
import unittest
from appium import webdriver
from base.mLog import myLog

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def initDriver(config):
    print("initDriver...")
    caps = {}
    if str(config["platformName"]).lower() == "android":
        caps['appPackage'] = config["appPackage"]
        caps['appActivity'] = config["appActivity"]
        caps['udid'] = config["deviceName"]
        caps["recreateChromeDriverSessions"] = "True"
        # caps["automationName"] = "uiautomator2"
    else:
        caps['bundleId'] = config["bundleId"]
        caps['udid'] = config["udid"]

    # caps['platformVersion'] = devices["platformVersion"]
    caps['platformName'] = config["platformName"]
    #     caps["automationName"] = devices['automationName']
    caps['deviceName'] = config["deviceName"]
    caps["noReset"] = "False"  # 每次都清缓存
    caps['noSign'] = "True"
    caps["unicodeKeyboard"] = "True"
    # caps["resetKeyboard"] = "True"
    # caps['simpleConfig'] = devices["simpleConfig"]
    # remote = "http://127.0.0.1:" + str(config["port"]) + "/wd/hub"
    remote = "http://127.0.0.1:{}/wd/hub".format(config["port"])
    driver = webdriver.Remote(remote, caps)  # 初始化时，确保手机和pc连接正常 且 为解锁状态
    driver.implicitly_wait(10)  # 隐式等待
    print("initDriver ok...")
    return driver


class MTestCase(unittest.TestCase):

    config = None
    def __init__(self, methodName='runTest', dconfig=None):
        print("MyTestCase init")
        super(MTestCase, self).__init__(methodName)
        global config
        config = dconfig

    # 整个Test类的开始执行

    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        cls.driver = initDriver(cls.config)
        # cls.devicesName = fullConfig["deviceName"]
        # cls.logger = myLog().getLog(cls.devicesName)  # 为每个设备实例化一个日志记录器
        print("setUpClass ok")

    # 每个用例的开始和结束执行
    # def setUp(self):
    #     print("MyTestCase-->setUp")
    #     pass

    # 整个Test类的结束执行
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def tearDown(self):
        # self.driver.quit()
        pass

    @staticmethod
    def load_tests(clz, param):
        """
        根据类名称，获取类中的测试方法
        :param clz: 类名称
        :param param:
        :return: 返回类中的测试方法
        """
        print("load_tests")
        testloader = unittest.TestLoader()
        # 获取clz类的所有测试方法
        testcaseNames = testloader.getTestCaseNames(clz)
        if len(testcaseNames) > 0:
            suite = unittest.TestSuite()
            for name in testcaseNames:
                # clz 继承MyTestCase,调用了MTestCase的构造方法,所以先执行MyTestCase
                suite.addTest(clz(name, param=param))
        else:
            print("there is no test in {}".format(clz))
        return suite
