# encoding=utf-8
from base.mAttr import Attr


class AppiumAPI:

    """
    appium api
    """
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, findType, elementInfo):
        """
        查找单个元素
        :param findType:
        :param elementInfo:
        :return:查询到的元素
        """
        print("正在查找元素：%s,查找方式：%s" % (elementInfo, findType))
        # 根据提供的关键字，区分对应的查找方式
        dict = {
            Attr.ID: lambda: self.driver.find_element_by_id(elementInfo),
            Attr.XPATH: lambda: self.driver.find_element_by_xpath(elementInfo),
            Attr.CLASS: lambda: self.driver.find_element_by_class_name(elementInfo),
            Attr.ACCESSIBILITY: lambda: self.driver.find_element_by_accessibility_id(elementInfo),
            Attr.TEXT: lambda: self.driver.find_element_by_android_uiautomator("text(\"" + elementInfo + "\")")
        }
        element = None
        try:
            element = dict[findType]()
            # return dict[findType]()  # 如果找到，则返回查询到的页面元素
        except Exception:
            import warnings
            warnings.warn("{} is not found".format(elementInfo))
        finally:
            return element

    def find_elements(self, findType, elementInfo, index):
        """
        查找多个元素时，使用index标明取得第几个
        :param findType:
        :param elementInfo:
        :param index:
        :return:
        """
        print("正在查找元素：%s,查找方式：%s,索引：%s" % (elementInfo, findType, index))
        # 根据提供的关键字，区分对应的查找方式
        dict = {
            Attr.ID: lambda: self.driver.find_elements_by_id(elementInfo),
            Attr.XPATH: lambda: self.driver.find_elements_by_xpath(elementInfo),
            Attr.CLASS: lambda: self.driver.find_elements_by_class_name(elementInfo),
            Attr.ACCESSIBILITY: lambda: self.driver.find_elements_by_accessibility_id(elementInfo),
            Attr.TEXT: lambda: self.driver.find_elements_by_android_uiautomator("text(\"" + elementInfo + "\")")
        }
        try:
            return dict[findType]()[int(index)]  # 如果找到，则返回查询到的页面元素
        except Exception:
            return None  # 如果没找到，返回False,不抛错

    def click(self, mobileElement, case=None):
        """
        执行点击
        :param mobileElement:
        :param case:
        :return:
        """
        mobileElement.click()

    def sendKeys(self, mobileElement, case):
        """
        输入文本
        :param mobileElement:
        :param case:
        :return:
        """
        data = case[Attr.DATA]  # excel 中的测试数据

        # excel中的数值会自动转为float，所以做下判断
        if type(data) == float:
            data = int(data)
        mobileElement.send_keys(data)

    def tap(self, case):
        """
        点击指定坐标，前面务必加上延时或者判断！
        # self.driver.tap([(100, 200)], 500) 单指操作
        # self.driver.tap([(100, 20), (100, 60), (100, 100)], 500) 多指操作
        :param case:
        """
        import time
        time.sleep(2)
        x, y = case[Attr.DATA]
        self.driver.tap([(x, y)], 500)

    def pressKeyCode(self, case):
        code = case[Attr.DATA]
        self.driver.press_keycode(keycode=int(code))

    def swipe(self, data):
        """
        :param data: (100,500,800,500,500)
        :return: exec swipe action
        """
        if len(data)==5:
            start_x, start_y, end_x, end_y, duration = data
            self.driver.swipe(self, start_x, start_y, end_x, end_y, duration=duration)
        elif len(data)==4:
            start_x, start_y, end_x, end_y= data
            self.driver.swipe(self, start_x, start_y, end_x, end_y, duration=500)
        else:
            pass


    def waitActivity(self, activity):
        i = 0
        while True:
            if self.driver.current_activity == activity:
                return True
            import time
            time.sleep(1)
            i += 1
            if i > 10:
                return False
