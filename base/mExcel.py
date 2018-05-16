# -*- coding: utf-8 -*-
import datetime
import xlrd
import xlwt
from xlsxwriter import workbook


class MyExcel:

    # 两个参数必传
    def __init__(self, path, sheetName):
        self.path = path
        self.sheetName = sheetName
        try:
            self.workbook = xlrd.open_workbook(self.path)
            self.sheet = self.sheet_by_name(self.sheetName)
        except Exception as e:
            print("请检查Excel文件是否存在，文件格式是否正确,提供的路径：", self.path)

    # 获取excel中所有sheet名称
    def sheet_names(self):
        return self.workbook.sheet_names()

    # 根据sheet名称获取sheet
    def sheet_by_name(self, sheetName):
        sheet = None
        try:
            sheet = self.workbook.sheet_by_name(sheetName)
        except Exception as e:
            print("没有找到sheet：", sheetName)
        return sheet

    def row_values(self, row):
        return self.sheet.row_values(row)



    def getCell(self, row, col):
        """
        用途：通过行列获取单元格，主要用于判断单元格的内容类型
        类型：ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        :param row: 行号
        :param col: 列号
        :return: 值
        """
        return self.sheet.cell(row, col)

    # 获取所有用例信息，每一行为一个用例
    def get_all_steps(self):
        rows = self.sheet.nrows  # 获取sheet的行数
        cases = []
        for r in range(rows):
            if r == 0: continue  # 去掉第一行标题
            case = self.sheet.row_values(r)  # 获取该行的内容[]
            cases.append(case)
        return cases

    def getTitle(self):
        title = self.sheet.row_values(0)
        print(len(title))
        dict = {}
        dict["id"] = title[0]
        dict["caseinfo"] = title[1]
        dict["step"] = title[2]
        dict["testinfo"] = title[3]
        dict["testpage"] = title[4]
        dict["pageinfo"] = title[5]
        dict["location"] = title[6]
        dict["element"] = title[7]
        dict["operation"] = title[8]
        dict["testdata"] = title[9]
        dict["checkdata"] = title[10]
        return dict


if __name__ == '__main__':
    excel = MyExcel("./my.xls", "登录")
    # cases = excel.get_all_steps()
    # print(cases)
    valueList = excel.row_values(3)
    value = valueList[10]
    print("type:", type(value), "value:", value)
    print(value == "")
    value = {"result": False}
    if value.get("result"):
        print("ok")
    # 判断值的类型，int自动转为float
    if type(value) == float:
        value = int(value)
    print(value)

    """ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error  """
    cell = excel.getCell(3, 9)
    print(cell.ctype)
