'''
Created on 2017年9月13日

@author: cm
'''
import unittest

from appium import webdriver

class DriverManage():

    def __init__(self,url,port,deviceName):
        self.url = url
        self.port = port
        self.deviceName = deviceName
        
    def initDriver(self,):
        print('start')
        desired_caps = {} # 定义一个字典
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = self.deviceName
        desired_caps['appPackage'] = 'com.tude.android'
        desired_caps['appActivity'] = '.base.SplashActivity'
        desired_caps["noReset"] = "False"
        # 'http://127.0.0.1:4723/wd/hub'
        self.driver = webdriver.Remote('http://'+self.url+':'+self.port+'/wd/hub', desired_caps)
        self.driver.implicitly_wait(15)
        print(self.deviceName,self.url,self.port)

    def quitDriver(self):
        self.driver.quit()

    def testFind(self):

        try:
            allow = self.driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button")
            for i in range(4):
                allow.click()
        except Exception:
            pass
        elments = self.driver.find_elements_by_class_name("android.widget.TextView")
        print("len:",len(elments),"type:",type(elments))
        elments[1].click()

    def api(self):

        # 查找元素
        self.driver.find_element_by_id()
        self.driver.find_element_by_name()
        self.driver.find_element_by_accessibility_id()
        self.driver.find_element_by_class_name()

        #
        self.driver.current_activity


        #
        self.driver.page_source()


        # find_elements
        self.driver.find_elements_by_id()
        self.driver.find_elements_by_android_uiautomator()
        self.driver.find_elements_by_accessibility_id()
        self.driver.find_elements_by_class_name()

if __name__ == '__main__':
    manage = DriverManage("127.0.0.1","4725","LE67A06310143950")
    manage.initDriver()
    manage.testFind()
    # manage.quitDriver()