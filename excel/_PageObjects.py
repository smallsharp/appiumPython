from excel._BaseExcel import BaseExcel
from excel._MyOperation import MyOperation
import unittest



class PageObjects:
    """
    page层：
    通过提供的Excel路径和Sheet，解析Excel
    """

    def __init__(self, driver, path, sheetName):
        self.driver = driver
        self.path = path
        self.sheetName = sheetName
        self.operation = MyOperation(self.driver)
        self.isOperate = True  # 操作失败，检查点就失败
        excel = BaseExcel(path=self.path, sheetName=self.sheetName)
        self.steps = excel.get_all_steps()  # 所有需要执行的用例信息

    def parse_case(self):
        # 遍历解析Excel中的用例信息
        checkSuccess = 0
        for step in self.steps:
            res = self.operation.operate(step)
            if res and res.get("result") is True:
                # checkSuccess += 1
                pass
            else:
                print("[失败详情]：", self.operation.getTestResult())
                return False
                # break
        return True


    def countSum(result):
        data = {"sum": 0, "pass": 0, "fail": 0}
        data["sum"] = data["sum"] + 1
        if result:
            data["pass"] = data["pass"] + 1
        else:
            data["fail"] = data["fail"] + 1

    def checkPoint(self, **kwargs):
        pass

    def check(self, **kwargs):
        for case in self.steps:
            self.operation.check(case=case)
