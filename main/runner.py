import unittest
from multiprocessing import Pool
from base.mAppiumServer import Server
from base.mTestCase import MTestCase
from base.mAppiumConfig import AppiumConfig
from cases.caseLogin import Login
from cases.caseLogin import Logout
from report import HTMLTestReportCN


# 多线程运行
def run_multiple(configList):
    fConfigList = []  # 完整的configList，多线程需要的配置
    for i in range(0, len(configList)):
        fconfig = {}
        fconfig["deviceName"] = configList[i]["deviceName"]
        fconfig["platformName"] = "android"
        fconfig["port"] = configList[i]["port"]
        fconfig["appPackage"] = "com.tude.android"
        fconfig["appActivity"] = ".base.SplashActivity"
        # config["automationName"] = "uiautomator2"
        fConfigList.append(fconfig)
    pool = Pool(len(fConfigList))
    pool.map(run_case, fConfigList)
    pool.close()
    pool.join()


# 执行用例，具体的用例类
def run_case(config):
    print("full_config:", config)
    # {'deviceName': 'GWY0217826005102', 'platformName': 'android', 'port': '4723', 'appPackage': 'com.tude.android', 'appActivity': '.base.SplashActivity'}
    suite = unittest.TestSuite()
    MTestCase.loadConfig(config)
    suite.addTest(MTestCase.load_tests(Login, param=config))
    suite.addTest(MTestCase.load_tests(Logout, param=config))
    # unittest.TestLoader.loadTestsFromTestCase(Login)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 确定生成报告的路径
    filePath = r'E:\测试报告.html'
    fp = open(filePath, 'wb')
    # 生成报告的Title,描述
    runner = HTMLTestReportCN.HTMLTestRunner(
        stream=fp,
        title='自动化测试报告',
        # description='详细测试用例结果',
        tester='Lee'
    )
    # 运行测试用例
    runner.run(suite)
    # 关闭文件，否则会无法生成文件
    fp.close()


if __name__ == '__main__':
    print("测试开始")
    configList = AppiumConfig.init()
    server = Server(configList)  # 启动服务可以放到远程服务器
    server.start()
    run_multiple(configList)
    server.stop(configList)
