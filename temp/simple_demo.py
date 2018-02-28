# coding=utf-8

# 一个最最简单的使用appium client进行操作的例子
from appium import webdriver
import subprocess

# build desired caps
desired_caps = {}
desired_caps['deviceName'] = '85GBBMA2353T'
desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = 25
desired_caps['appPackage'] = 'com.tencent.wstt.gt'
desired_caps['appActivity'] = '.activity.SplashActivity'  # 前面不要加上包名
# desired_caps['dontStopAppOnReset'] = True
desired_caps['noReset'] = True
# desired_caps['stopAppAtEnd'] = False
desired_caps['autoUnlock'] = False
# desired_caps['newCommandTimeout'] = 600

# start server
appium_path = r"D:\nodejs\new_modules\appium.cmd"
server_cmd = appium_path + ' -p 26270 -bp 27235 -U 85GBBMA2353T --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
server = subprocess.Popen(server_cmd, shell=True)
# import os
# server = os.system(server_cmd)


# init driver
driver = webdriver.Remote('http://localhost:26270/wd/hub', desired_caps)


import time
time.sleep(2)

# do something
# driver.swipe(100, 100, 200, 200, 500)
driver.press_keycode(keycode=3)
print("click home button")


# after all
driver.quit()
server.kill()
