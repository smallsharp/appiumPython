# -*- coding=utf-8 -*-
'''*********************************************************************************************************************
@名称介绍:
@功能说明:获取地址获取excel，定义获取sheet，行，内容
@参数说明:
@返回结果:
@调用示例:
*********************************************************************************************************************'''
import xlrd
import os
from xlutils.copy import copy


class OpenExcel():
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
            try:
                self.data = self.get_data()
                print("data:", self.data)
            except Exception as e:
                print("请提供正确格式的Excel文件！")
        else:
            print("文件路径不能为空！")
        # 获取sheet内容

    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        table = data.sheets()[self.sheet_id]
        return table
        # 获取单元格行数

    def get_sheet_lins(self):
        table = self.data
        return table.nrows
        # 获取某一个单元格的内容

    def get_all_value(self, row, col):
        return self.data.cell_value(row, col)
        # 写入excel数据

    def write_value(self, row, col, value):
        read_excel = xlrd.open_workbook(self.file_name)
        write_excel = copy(read_excel)
        sheet_excel = write_excel.get_sheet(0)
        sheet_excel.write(row, col, value)
        write_excel.save(self.file_name)

        # 根据对应的numberID找到行的内容

    def get_rows_data(self, case_id):
        pass
        # 根据对应的numberid找到对应的行号

    def get_row_num(self, case_id):
        pass
        # 根据行号，找到该行的内容

    def get_row_value(self, row):
        pass


if __name__ == '__main__':
    # excel = OpenExcel()
    # data = excel.get_data()
    # print(excel.get_all_value(2, 0))

    excel = OpenExcel("11.xls", 1)
    print(excel.get_all_value(0,0))
    print(excel.get_sheet_lins())
    print(excel.get_row_num("测试页面"))
