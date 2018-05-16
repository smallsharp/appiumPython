# coding=utf-8

from appium import webdriver
import subprocess


# 入门Demo
# 85GBBMA2353T


class Demo:

    def __init__(self):
        # 1.build desired caps
        self.driver = self.initDriver()


    def initDriver(self):
        # 1.build desired caps
        desired_caps = {}
        desired_caps['deviceName'] = 'GWY0217826005102'
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = 25
        desired_caps['appPackage'] = 'com.tude.android'
        desired_caps['appActivity'] = '.base.SplashActivity'  # 前面不要加上包名
        # desired_caps['dontStopAppOnReset'] = True
        desired_caps['noReset'] = True
        # desired_caps['stopAppAtEnd'] = False
        desired_caps['autoUnlock'] = False
        # desired_caps['newCommandTimeout'] = 600

        # 2.start server
        appium_path = r"D:\nodejs\new_modules\appium.cmd"
        server_cmd = appium_path + ' -p 4723 -bp 27235 -U GWY0217826005102 --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
        self.server = subprocess.Popen(server_cmd, shell=True)
        # import os
        # server = os.system(server_cmd)

        # 3. init driver
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        return driver

    # 4.do something
    def test(self):
        import time
        time.sleep(5)

        # driver.swipe(100, 100, 200, 200, 500)
        # driver.press_keycode(keycode=3)
        # driver.tap([(100, 20), (100, 60), (100, 100)], 500)

        self.driver.find_element_by_id('com.tude.android:id/btn_profile').click()

        time.sleep(2)

        # self.driver.tap([(100, 200)], 500)
        self.driver.tap([(300, 300), (600, 600), (900, 900)], 500)
        time.sleep(2)

        self.driver.swipe()

        # self.driver.find_element_by_id('com.tude.android:id/btn_cart').click()
        # driver.tap([(100, 20), (100, 60), (100, 100)], 500)
        time.sleep(2)

    def teardown(self):
        self.driver.quit()
        self.server.kill()



try:
    demo = Demo()
    demo.test()
    demo.teardown()
except Exception as e:
    print(e)

