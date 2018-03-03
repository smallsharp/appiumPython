# -*- coding: utf-8 -*-
import time
from appium import webdriver
import unittest
import os
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class _AppiumDemo(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'         # 设备系统
        desired_caps['deviceName'] = 'LE67A06310143950'    # 设备名称
        desired_caps['appPackage'] = 'com.tude.android'         # 应用的包名
        desired_caps['appActivity'] = '.base.SplashActivity'         # 应用启动需要的Android Activity名称
        # desired_caps["noReset"] = "True"
        # desired_caps['noSign'] = "True"         # 跳过检查核对应用进行debug的签名的步骤
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        desired_caps["automationName"] = "Appium"
        remote = "http://127.0.0.1:4723" + "/wd/hub"         # 配置远程server（通过本地代码调用远程server）
        print(remote)
        self.driver = webdriver.Remote(remote, desired_caps)

    def test_search(self):
        input = self.driver.find_element_by_id('url')
        input.send_keys('http://wap.sogou.com')
        search_button = self.driver.find_element_by_id("searchbutton")
        search_button.click()
        time.sleep(3)
        print(self.driver.contexts)
        self.driver.switch_to.context("WEBVIEW_0")
        print(self.driver.contexts)
        time.sleep(3)
        webinput = self.driver.find_element_by_xpath('//*[@id="keyword"]')
        webinput.click()
        webinput.send_keys('mook')
        web_search_button = self.driver.find_element_by_xpath('//*[@id="searchform"]/div/div/div[1]/div[3]/input')
        web_search_button.click()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()





