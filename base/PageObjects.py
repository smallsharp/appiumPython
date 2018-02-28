import time
from base.BaseProperties import BaseProperties as attr
from base.BaseYaml import loadYaml
from base.Operation import Operation
from base.BaseStatistics import countSum, countInfo


class PageObjects:

    '''
    page层
    解析yaml文件
    '''
    def __init__(self, **kwargs):
        self.driver = kwargs["driver"]
        self.path = kwargs["path"]
        # if kwargs.get("launch_app", "0") == "0":  # 若为空，重新打开app
        #     self.driver.launch_app()
        self.operation = Operation(self.driver)
        self.isOperate = True # 操作失败，检查点就失败
        fileContent = loadYaml(self.path)
        self.testInfo = fileContent[attr.TEST_INFO] # 文本中的testinfo
        self.testCase = fileContent[attr.TEST_CASE] # 文本中的testcase
        self.testCheck = fileContent[attr.CHECK] # 文本中的check
        self.get_value = []
        self.is_get = False  # 检查点特殊标志，结合get_value使用。若为真，说明检查点要对比历史数据和实际数据
        self.msg = ""

    '''
     操作步骤
     logTool 日记记录器
     case对应testcase类目下的具体的单个case，like follows:
    - element_info: com.tude.android:id/btn_profile
      find_type: id
      operate_type: click
      info: 点击我的
    '''
    def parseTestCase(self, logger):
        for case in self.testCase:
            msg_ = self.msg + "\n" if self.msg != "" else ""
            print("msg_:",msg_)
            result = self.operation.operate(case, self.testInfo, logger)
            if not result["result"]:
                msg = "执行过程中失败，没有找到元素：" + case[attr.ELEMENT_INFO]
                if not result.get("webview", True):
                    msg = "切换到webview失败，请确定是否在webview页面"
                print("msg:",msg)
                self.msg = msg_ + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False
            if case.get("is_time", "0") != "0":
                time.sleep(case["is_time"])  # 等待时间
                print("--等待下---")

            if case.get(attr.OPERATE_TYPE, "0") == attr.GET_VALUE or case.get(attr.OPERATE_TYPE, "0") == attr.GET_CONTENT_DESC :
                self.get_value.append(result["text"])
                self.is_get = True  # 对比数据
        return True

    def checkPoint(self, **kwargs):
        result = self.check(**kwargs)
        if result is not True and attr.RE_CONNECT:
            self.msg = "用例失败重连过一次，失败原因:" + self.testInfo[0]["msg"]
            kwargs["logger"].buildStartLine(kwargs["caseName"]+"_失败重连")  # 记录日志
            self.operation.switchToNative()
            self.driver.launch_app()
            self.isOperate = True
            self.get_value = []
            self.is_get = False
            self.parseTestCase(kwargs["logger"])
            result = self.check(**kwargs)
            self.testInfo[0]["msg"] = self.msg
        self.operation.switchToNative()
        countSum(result)
        countInfo(result=result, testInfo=self.testInfo, caseName=kwargs["caseName"],
                  driver=self.driver, logTest=kwargs["logger"], devices=kwargs["devices"], testCase=self.testCase,
                  testCheck=self.testCheck)
        return result

    '''
    检查点
    caseName:测试用例函数名 用作统计
    logger： 日志记录
    devices 设备名
    contrary：相反检查点，传1表示如果检查元素存在就说明失败
    toast: 表示提示框检查点
    contrary_getval: 相反值检查点，如果对比成功，说明失败
    check: 自定义检查结果
    excepts: 如果为1，表示操作出现异常情况检查点为成功
    '''

    def check(self, **kwargs):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""
        # 如果有重跑机制，成功后会默认把日志传进来
        # if kwargs.get("check", "0") != "0":
        #     return kwargs["check"]

        if self.isOperate:
            for item in self.testCheck:
                if kwargs.get("toast", "0") != "0":
                    resp = self.operation.toast(item[attr.ELEMENT_INFO], testInfo=self.testInfo,
                                                logTest=kwargs["logger"])
                else:
                    resp = self.operation.operate(item, self.testInfo, kwargs["logger"])

                if kwargs.get("excepts", "0") != "0" and not resp["result"]:
                    print("操作失败，简单点为成功")
                    result = True
                    break

                if kwargs.get("contrary", "0") != "0" and resp["result"]:
                    m = "请检查%s" % item["info"] + "是否成功"
                    self.msg = m_s_g + m
                    print(self.msg)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
                if kwargs.get("contrary", "0") == "0" and not resp["result"]:
                    m = "请检查元素" + item[attr.ELEMENT_INFO] + "是否存在"
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break

                if kwargs.get("contrary_getval", "0") != "0" and self.is_get and resp["result"] in self.get_value:
                    result = False
                    m = "对比数据失败，当前取到到数据为:%s,历史取到数据为:%s" % resp["text"] % self.get_value
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    break

                if kwargs.get("contrary_getval",
                              "0") == "0" and self.is_get and resp["text"] not in self.get_value:  # 历史数据和实际数据对比
                    result = False
                    m = "对比数据失败,获取历史数据为：" + ".".join(self.get_value) + ",当前获取的数据为：" + resp["text"]
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    break
        else:
            result = False
        return result
