from base.mExcel import MyExcel
from base.mOperation import MyOperation


class PageObjects:
    """
    page层：
    通过提供的Excel路径和Sheet，解析Excel
    """

    def __init__(self, driver, path, sheetName):
        excel = MyExcel(path=path, sheetName=sheetName)
        self.steps = excel.getAllSteps()  # 所有需要执行的用例信息
        self.operation = MyOperation(driver)
        # self.operation = MyOperation(driver,self.steps)


    def execCase(self):
        # 遍历解析Excel中的用例信息
        for step in self.steps:
            res = self.operation.execStep(step)
            if res and res.get("result") is True:
                pass
            else:
                print("[失败详情]：", self.operation.getTestResult())
                return False
        return True
