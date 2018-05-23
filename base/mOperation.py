# -*- coding: utf-8 -*-
from time import sleep
from base.mAttr import Attr as attr
from base.mExcel import MyExcel
from base.mAppiumAPI import AppiumAPI


class MyOperation:

    """
    主要用于用例的执行驱动，执行用例相关操作
    具体操作,根据解析Excel中的关键字，判断执行何种操作，如查找元素，输入等
    """
    def __init__(self, driver, steps=None):
        """
        生成一个用例执行驱动实例
        :param driver: 可执行用例的实例对象
        """
        self.driver = driver
        self.api = AppiumAPI(self.driver)
        # self.steps = steps

    def execStep(self, step):
        """
        用例执行入口，分发任务
        :param step: 需要执行的用例，对应sheet中一行
        :return: 执行后的断言结果
        """
        find_type = step[attr.FIND_TYPE]  # 取Excel中的定位方式列中的值
        operate_type = step[attr.OPERATE_TYPE]
        element_info = step[attr.ELEMENT_INFO]
        check_type = step[attr.CHECK_TYPE]
        check_expect = step[attr.CHECK_EXPECT]
        index = step[attr.ELEMENT_INDEX]
        print("===>>：", step)

        # 判断 操作方式是否为空
        if operate_type == "":
            raise RuntimeError("operateType是必要参数，你传的是：", operate_type)

        # 判断 操作方式是否需要元素
        elif operate_type in [attr.CLICK, attr.SEND_KEYS]:
            if not element_info:
                raise RuntimeError(
                    "缺少必要的参数{find_type},{element_info}".format(find_type=find_type, element_info=element_info))
            if index:
                mobile_element = self.api.find_elements(find_type,element_info,index)
            else:
                mobile_element = self.api.find_element(find_type,element_info)
            if mobile_element:
                print("Found Element：", element_info)
                self.do_action_with_element(step=step, operate_type=operate_type, mobile_element=mobile_element)
            else:
                print("Element Not Found：", element_info)  # 元素没找到的情况下，记录日志

        # 操作方式不需要元素的，如presskeycode,swipe,tap等
        else:
            self.do_action(case=step, operateType=operate_type)

        #  所有操作执行完毕后，判断是否需要断言(检查类型和预期结果 均存在才执行断言)
        if check_type and check_expect:
            result = self.check(check_type, check_expect).get("result")
            # self.summury(result, checkType=check_type, checkExpect=check_expect)  # 汇总断言数据
            if result:
                return {"result": True}
            return {"result": False}
        # print("TestResult:", self.getTestResult())
        return {"result": True}  # 没有标明需要断言，直接返回True

    def do_action(self, case, operateType):
        """
        执行何种操作（api封装）
        :param case:
        :param operateType:
        :return:
        """
        action = {
            attr.SWIPE: lambda: self.api.swipe(case),
            attr.TAP: lambda: self.api.tap(case),
            attr.PRESS_KEY_CODE: lambda: self.api.pressKeyCode(case)
        }
        return action[operateType]()

    def do_action_with_element(self, operate_type, mobile_element, step):
        """
        执行何种操作（需要提供元素）
        :param operate_type:
        :param mobile_element:
        :param step:
        :return:
        """
        action = {
            attr.CLICK: lambda: self.api.click(mobile_element,case=step),
            attr.SEND_KEYS: lambda: self.api.sendKeys(mobile_element,case=step),
        }
        return action[operate_type]()

    failList = []

    def check(self, checkType, checkExpect):
        """
        断言
        :param checkType:
        :param checkExpect:
        :return:
        """
        if checkType == attr.CHECK_PAGE:
            print("current:%s,expect:%s" % (self.driver.current_activity, checkExpect))
            currentPage = self.driver.current_activity
            if currentPage == checkExpect:
                return {"result": True}  # 断言通过
            self.failList.append(self.failDetail(checkType, checkExpect, currentPage))

        elif checkType == attr.CHECK_ID:
            try:
                element = self.driver.find_element_by_id(checkExpect)
                if element:
                    return {"result": True}
                self.failList.append(self.failDetail(checkType, checkExpect, element))
            except Exception as e:
                pass  # 没有找到元素不返回{"result": True}
        elif checkType == attr.CHECK_TEXT:
            if self.checkText(checkExpect=checkExpect).get("result"):
                return {"result": True}
            self.failList.append(self.failDetail(checkType, checkExpect, None))
        else:
            raise RuntimeError("没有提供这种断言方式：", checkType)

        return {"result": False}

    def failDetail(self, checkTpye, checkExpect, actual=None):
        message = "AssertFail，断言方式：{}，预期数据：{}，实际：{}".format(checkTpye, checkExpect, actual)
        print(message)
        return message

    TestResult = []

    def summury(self, result, checkType, checkExpect, actual=None):
        itemDict = {}
        itemDict["result"] = result
        itemDict["checkType"] = checkType
        itemDict["checkExpect"] = checkExpect
        itemDict["actual"] = actual
        self.TestResult.append(itemDict)

    def getTestResult(self):
        return self.TestResult

    def checkText(self, checkExpect):
        """
        辅助断言
        :param checkExpect:
        :return:
        """
        try:
            # 通过text查找元素，查询元素
            if self.driver.find_element_by_android_uiautomator("text(\"" + checkExpect + "\")"):
                print("通过find_element_by_android_uiautomator，断言通过：", checkExpect)
                return {"result": True}
            # 通过discription，查找元素
            elif self.driver.find_element_by_accessibility_id(checkExpect):
                print("通过find_element_by_accessibility_id，断言通过：", checkExpect)
                return {"result": True}
            # 通过整个页面查找元素
            elif self.driver.page_source.find(checkExpect) != -1:
                print("通过page_source，断言通过：", checkExpect)
                return {"result": True}
            else:
                return {"result": False}  # 没有找到元素返回{"result": False}
        except Exception:
            return {"result": False}  # 没有找到元素返回{"result": False}


if __name__ == '__main__':
    op = MyOperation()
    excel = MyExcel("my.xls", "登录")
    cases = excel.getAllSteps()
    print(cases)
    op.execStep(cases)
