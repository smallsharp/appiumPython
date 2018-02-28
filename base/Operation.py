# coding=utf-8
import re
import os
import time
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from base.BaseProperties import BaseProperties as attr

'''
# 此脚本主要用于查找元素，操作页面元素
'''


class Operation:
    def __init__(self, driver=""):
        self.driver = driver
    '''
    查找元素.case是字典
    operate_type：对应的操作
    element_info：元素详情
    find_type: find类型
    testInfo: 用例单个步骤信息
    logT: 记录日志
    '''
    def operate(self, case, testInfo, logger):
        print("[第一步]：执行operate：",case)
        # 执行查找元素
        res = self.findElement(case)
        # 查看返回是否成功 res: {'result': True}
        if res["result"]:
            # 执行何种操作
            return self.operate_by(case, testInfo, logger)
        else:
            return res

    def findElement(self, case):
        print("[第二步]：执行findElement")
        #{'element_info': 'com.tude.android:id/btn_profile', 'find_type': 'id', 'operate_type': 'click', 'info': '点击我的', 'is_time': 2}
        try:
            if type(case) == list:  # 多检查点
                for item in case:
                    if item.get("is_webview", "0") == 1:  # 1表示切换到webview
                        self.switchToWebview()
                    elif item.get("is_webview", "0") == 2:
                        self.switchToNative()
                    # if item.get(attr.ELEMENT_INFO, "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                    #     return {"result": True}
                    time = item[attr.CHECK_TIME] if item.get(attr.CHECK_TIME, "0") != "0" else attr.WAIT_TIME
                    WebDriverWait(self.driver, time).until(lambda x: self.findElementBy(item))
                return {"result": True}

            if type(case) == dict:  # 单检查点
                # 1表示切换到webview
                if case.get("is_webview", "0") == 1 and self.switchToWebview() is False:
                    print("切换到webview失败，请确定是否在webview页面")
                    return {"result": False, "webview": False}
                elif case.get("is_webview", "0") == 2:
                    self.switchToNative()
                if case.get(attr.ELEMENT_INFO, "0") == "0":  # 如果没有页面元素，就不检测是页面元素，可能是滑动等操作
                    return {"result": True}
                # 如果自定义检测时间为空，就用默认的检测等待时间
                time = case["check_time"] if case.get("check_time","0") != "0" else attr.WAIT_TIME
                # 通过case中find_type类型，查找元素
                WebDriverWait(self.driver, time).until(lambda x: self.findElementBy(case))
                print("[第三步]：",case[attr.ELEMENT_INFO],"元素找到了！")
                return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            # print("查找元素" + case[attr.ELEMENT_INFO] + "超时")
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            # print("查找元素" + case[attr.ELEMENT_INFO] + "不存在")
            return {"result": False}


    def operate_by(self, case, testInfo, logger):
        print("[第四步]：","执行何种操作：",case.get(attr.OPERATE_TYPE))
        try:
            # 拼接元素属性 和 执行的动作属性，使用“-”等
            info = case.get(attr.ELEMENT_INFO, " ") + "_" + case.get(attr.OPERATE_TYPE, " ") + str(case.get(
                "code", " ")) + case.get("msg", " ")
            logger.buildStartLine(testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + info)  # 记录日志
            print("info:",info)
            if case.get(attr.OPERATE_TYPE, "0") == "0":  # 如果没有此字段，说明没有相应操作，一般是检查点，直接判定为成功
                return {"result": True}

            # 执行何种操作
            action = {
                attr.SWIPE_DOWN: lambda: self.swipeToDown(),
                attr.SWIPE_UP: lambda: self.swipeToUp(),
                attr.CLICK: lambda: self.click(case),
                attr.GET_VALUE: lambda: self.get_value(case),
                attr.SET_VALUE: lambda: self.set_value(case),
                attr.ADB_TAP: lambda: self.adb_tap(case),
                attr.GET_CONTENT_DESC: lambda: self.get_content_desc(case),
                attr.PRESS_KEY_CODE: lambda: self.press_keycode(case)
            }
            # 通过operate_type判断是何种操作
            return action[case.get(attr.OPERATE_TYPE)]()
        except IndexError:
            logger.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + case[attr.ELEMENT_INFO] + "索引错误")  # 记录日志
            print(case[attr.ELEMENT_INFO] + "索引错误")
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            logger.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + case[
                    attr.ELEMENT_INFO] + "页面元素不存在或没加载完成")  # 记录日志
            print(case[attr.ELEMENT_INFO] + "页面元素不存在或没有加载完成")

            return {"result": False}
        except selenium.common.exceptions.StaleElementReferenceException:
            logger.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + case[
                    attr.ELEMENT_INFO] + "页面元素已经变化")  # 记录日志
            print(case[attr.ELEMENT_INFO] + "页面元素已经变化")
            return {"result": False}
        except KeyError:
            # 如果key不存在，一般都是在自定义的page页面去处理了，这里直接返回为真
            return {"result": True}

    # 获取到元素到坐标点击，主要解决浮动层遮档无法触发driver.click的问题
    def adb_tap(self, case):
        bounds = self.findElementBy(case).location
        x = str(bounds["x"])
        y = str(bounds["y"])
        os.system("adb shell input tap " + x + " " + y)
        return {"result": True}

    def toast(self, xpath, logTest, testInfo):
        logTest.buildStartLine(testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + "查找弹窗元素_" + xpath)  # 记录日志
        try:
            WebDriverWait(self.driver, 10, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False}

    # 点击事件，区分点击具体还是多个中的一个
    def click(self, case):
        print("执行：click")
        # if case[attr.FIND_TYPE] == attr.find_element_by_id or case[attr.FIND_TYPE] == attr.find_element_by_xpath:
        #     self.findElementBy(case).click()
        # elif case.get(attr.FIND_TYPE) == attr.find_elements_by_id:
        #     self.findElementBy(case)[case["index"]].click()
        self.findElementBy(case).click()
        return {"result": True}

    # code 事件
    def press_keycode(self, case):
        self.driver.press_keycode(case.get("code", 0))
        return {"result": True}

    def get_content_desc(self, case):
        result = self.findElementBy(case).get_attribute("contentDescription")
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    '''
    切换native
    '''
    def switchToNative(self):
        self.driver.switch_to.context("NATIVE_APP")  # 切换到native

    '''
    切换webview
    '''
    def switchToWebview(self):
        n = 1
        while n < 10:
            time.sleep(3)
            n = n + 1
            print(self.driver.contexts)
            for cons in self.driver.contexts:
                if cons.lower().startswith("webview"):
                    self.driver.switch_to.context(cons)
                    # print(self.driver.page_source)
                    self.driver.execute_script('document.querySelectorAll("html")[0].style.display="block"')
                    self.driver.execute_script('document.querySelectorAll("head")[0].style.display="block"')
                    self.driver.execute_script('document.querySelectorAll("title")[0].style.display="block"')
                    print("切换webview成功")
                    return {"result": True}
        return {"result": False}

    # 左滑动
    def swipeLeft(self, case):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x1 = int(width * 0.75)
        y1 = int(height * 0.5)
        x2 = int(width * 0.05)
        self.driver(x1, y1, x2, y1, 600)

    # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    def swipeToDown(self):
        height = self.driver.get_window_size()["height"]
        x1 = int(self.driver.get_window_size()["width"] * 0.5)
        y1 = int(height * 0.25)
        y2 = int(height * 0.75)
        self.driver.swipe(x1, y1, x1, y2, 1000)
        # self.driver.swipe(0, 1327, 500, 900, 1000)
        print("--swipeToDown--")
        return {"result": True}

    def swipeToUp(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
        print("执行上拉")
        return {"result": True}
        # for i in range(n):
        #     self.driver.swipe(540, 800, 540, 560, 0)
        #     time.sleep(2)

    def swipeToRight(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        x1 = int(width * 0.05)
        y1 = int(height * 0.5)
        x2 = int(width * 0.75)
        self.driver.swipe(x1, y1, x1, x2, 1000)
        # self.driver.swipe(0, 1327, 500, 900, 1000)
        print("--swipeToUp--")

    def set_value(self, case):
        """
        输入值，代替过时的send_keys
        :param case:
        :return:
        """
        self.findElementBy(case).send_keys(case["msg"])
        return {"result": True}

    def get_value(self, case):
        '''
        读取element的值,支持webview下获取值
        :param case:
        :return:
        '''
        resutl = ""
        if case.get(attr.FIND_TYPE) == attr.find_elements_by_id:
            element_info = self.findElementBy(case)[case["index"]]
            if case.get("is_webview", "0") == 1:
                result = element_info.text
            else:
                result = element_info.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)  # 只匹配中文，大小写，字母
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.findElementBy(case)
        if case.get("is_webview", "0") == 1:
            result = element_info.text
        else:
            result = element_info.get_attribute("text")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    # 封装常用的标签
    def findElementBy(self, case):
        print("正在查找元素，findElementBy：",case[attr.ELEMENT_INFO])
        findTypes = {
            attr.find_element_by_id: lambda: self.driver.find_element_by_id(case[attr.ELEMENT_INFO]),
            attr.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(case[attr.ELEMENT_INFO]),
            attr.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(case['element_info']),
            attr.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(case['element_info']),
            attr.find_elements_by_id: lambda: self.driver.find_elements_by_id(case['element_info'])
        }
        return findTypes[case[attr.FIND_TYPE]]()
