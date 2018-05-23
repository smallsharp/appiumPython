# -*- coding: utf-8 -*-
import os
import unittest
from appium import webdriver
from base.mLog import myLog

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/caps.md
def initDriver(caps):
    print("initDriver...")
    # {'deviceName': 'LE67A06310143950', 'platformName': 'android', 'port': '4723'}
    newCaps = {}
    if str(caps["platformName"]).lower() == "android":
        newCaps['udid'] = caps["deviceName"]
        newCaps["recreateChromeDriverSessions"] = "True"
        newCaps["unicodeKeyboard"] = "True"  # unicode input
        newCaps["resetKeyboard"] = "True"  # reset keyboard after test
        # caps["automationName"] = "uiautomator2"
        newCaps['app'] = PATH('../app/taidu.apk')
        newCaps['appPackage'] = 'com.tude.android'
        newCaps['appActivity'] = '.base.SplashActivity' # 最好指定,从app解析出来的会带上appPackage,可能无法启动
    else:
        newCaps['bundleId'] = caps["bundleId"]
        newCaps['udid'] = caps["udid"]
        # caps["automationName"] = 'XCUITest'

    newCaps['platformName'] = caps["platformName"]
    newCaps['deviceName'] = caps["deviceName"]
    newCaps["noReset"] = "False"  # clear cache every time
    newCaps['noSign'] = "True"
    remote = "http://127.0.0.1:{}/wd/hub".format(caps["port"])
    driver = webdriver.Remote(remote, newCaps)  # 初始化时，确保手机和pc连接正常 且 为解锁状态
    driver.implicitly_wait(10)  # 隐式等待
    print("initDriver ok...")
    return driver


class MyTestCase(unittest.TestCase):

    config = None
    def __init__(self, methodName='runTest',mconfig=None):
        super(MyTestCase, self).__init__(methodName)
        global config
        config = mconfig

    # Test类的开始执行
    @classmethod
    def setUpClass(cls):
        cls.driver = initDriver(config)
        # cls.logger = myLog().getLog(config["deviceName"])

    # 每个用例开始时执行
    # def setUp(self):
    #     print("MyTestCase-->setUp")
    #     pass

    # Test类的结束执行
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 每个用例开始时执行
    def tearDown(self):
        pass

    @staticmethod
    def load_tests(clz, caps):
        """
        根据类名称，获取类中的测试方法
        :param clz: 类名称
        :param caps:
        :return: 返回类中的测试方法
        """
        testloader = unittest.TestLoader()
        # 获取clz类的所有测试方法
        testcaseNames = testloader.getTestCaseNames(clz)
        if len(testcaseNames) > 0:
            suite = unittest.TestSuite()
            for name in testcaseNames:
                # clz 继承MyTestCase,调用了MTestCase的构造方法,所以先执行MyTestCase
                suite.addTest(clz(name, caps)) # 实例化
        else:
            print("No Test Found in {}".format(clz))
        return suite
