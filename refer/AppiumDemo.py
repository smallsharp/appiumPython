# coding=utf-8

from appium import webdriver
import subprocess
import time


# 一个相对完整的例子

class Demo:

    def __init__(self):
        # self.startServer()
        self.driver = self.initDriver()

    # 1.start server
    def startServer(self):
        appium = r'D:\nodejs\new_modules\appium.cmd'
        cmd = appium + ' -p 4723 -bp 27235 -U LE67A06310143950 --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
        self.server = subprocess.Popen(cmd, shell=True)

    # 2.build driver
    def initDriver(self):
        desired_caps = {}
        desired_caps['deviceName'] = 'LE67A06310143950'
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = 25
        # desired_caps['app'] = '../taidu.apk' # refer the apk to be installed
        desired_caps['appPackage'] = 'com.tude.android'
        desired_caps['appActivity'] = '.base.SplashActivity'  # no packageName prefix
        desired_caps['noReset'] = 'true'
        # desired_caps['newCommandTimeout'] = 600
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        driver.implicitly_wait(10)
        return driver

    # 3.do somework
    def test(self):
        self.driver.find_element_by_id('com.tude.android:id/btn_profile').click()
        # self.driver.find_element_by_id('com.tude.android:id/et_account').send_keys('18521035133')
        # self.driver.find_element_by_id('com.tude.android:id/et_password').send_keys('111111')
        # self.driver.find_element_by_id('com.tude.android:id/btn_login').click()
        # assert self.driver.current_activity=='.base.HomeActivity'

    # 4. clear
    def teardown(self):
        self.driver.quit()
        # self.server.kill()


if __name__ == '__main__':

    try:
        demo = Demo()
        demo.test()
        demo.teardown()
    except Exception as e:
        print(e)
