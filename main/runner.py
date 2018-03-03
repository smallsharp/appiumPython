import unittest
from multiprocessing import Pool
from base.AppiumServer import AppiumServer
from base.BaseTestCase import MyTestCase
from base.AppiumConfig import AppiumConfig
from cases.Login import Login
from cases.Login import Logout
from report import HTMLTestReportCN


# 多线程运行
def run_multiple(simple_config):
    full_config_l = []  # 完整的configList，多线程需要的配置
    for i in range(0, len(simple_config)):
        full_config = {}
        full_config["deviceName"] = simple_config[i]["deviceName"]
        full_config["platformName"] = "android"
        full_config["port"] = simple_config[i]["port"]
        full_config["appPackage"] = "com.tude.android"
        full_config["appActivity"] = ".base.SplashActivity"
        # config["automationName"] = "uiautomator2"
        full_config_l.append(full_config)
    pool = Pool(len(full_config_l))
    pool.map(run_case, full_config_l)
    pool.close()
    pool.join()


# 执行用例，具体的用例类
def run_case(full_config):
    print("full_config:", full_config)
    # {'deviceName': 'GWY0217826005102', 'platformName': 'android', 'port': '4723', 'appPackage': 'com.tude.android', 'appActivity': '.base.SplashActivity'}
    suite = unittest.TestSuite()
    suite.addTest(MyTestCase.load_tests(Login, param=full_config))
    suite.addTest(MyTestCase.load_tests(Logout, param=full_config))
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
    simple_config_list = AppiumConfig.init_config()
    server = AppiumServer(simple_config_list)  # 启动服务可以放到远程服务器
    server.start()
    run_multiple(simple_config_list)
    server.stop(simple_config_list)
