import unittest
import os
from multiprocessing import Pool
from base.mAppiumServer import AppiumServer
from base.mTestCase import MyTestCase
from base.mAppiumConfig import AppiumConfig
from base.HTMLTestReportCN import HTMLTestRunner
from cases.personal import Login
from cases.shopping import OpenCart


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# 多线程运行
def runMultiple(devices):
    configs = []  # 完整的configs，多线程需要的配置
    for i in range(0, len(devices)):
        caps = {}
        caps["platformName"] = "android"
        caps["port"] = devices[i]["port"]
        caps["deviceName"] = devices[i]["deviceName"]
        configs.append(caps)
    pool = Pool(len(configs)) # thread pool
    pool.map(runCases, configs)
    pool.close()
    pool.join()


# 分线程执行用例
def runCases(config):
    # {'deviceName': 'GWY0217826005102', 'platformName': 'android', 'port': '4723', 'appPackage': 'com.tude.android', 'appActivity': '.base.SplashActivity'}
    # 添加测试用例
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase.load_tests(Login, config))
    suite.addTest(MyTestCase.load_tests(OpenCart, config))

    # 生成报告
    filePath = PATH('../report/{}.html'.format(config['deviceName']))
    fp = open(filePath, 'wb')
    # 生成报告的Title,描述
    runner = HTMLTestRunner(
        stream=fp,
        title='Test Report',
        description='Test Description',
        tester='Lee'
    )
    # 运行测试用例
    runner.run(suite)
    # 关闭文件，否则会无法生成文件
    fp.close()


if __name__ == '__main__':
    devices = AppiumConfig.init()
    server = AppiumServer(devices)  # 启动服务
    server.start()
    runMultiple(devices)
    server.stop(devices)
