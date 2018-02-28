# -*- coding: utf-8 -*-
import datetime
import xlrd
import xlwt
from xlsxwriter import workbook


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook("11.xls")

    # 获取该文件下所有sheet
    print("文件下的sheet：", workbook.sheet_names())  # [u'sheet1', u'sheet2']
    sheet1_name = workbook.sheet_by_name("测试机").name
    sheet2_name = workbook.sheet_names()[1]
    print("第一个sheet：", sheet1_name)
    print("第二个sheet：", sheet2_name)

    # 根据sheet索引或者名称获取sheet内容
    sheet1 = workbook.sheet_by_index(0)  # 通过索引获取sheet
    # sheet的名称，行数，列数快lj
    sheet2 = workbook.sheet_by_name('登录')  # 通过名字获取sheet
    # sheet的名称，行数，列数
    print("sheet1:%s, rows:%s, cols:%s" % (sheet1.name, sheet1.nrows, sheet1.ncols))
    print("sheet2:%s, rows:%s, cols:%s" % (sheet2.name, sheet2.nrows, sheet2.ncols))

    # 获取整行和整列的值（数组）
    rows0 = sheet2.row_values(0)  # 获取第0行内容
    cols8 = sheet2.col_values(8)  # 获取第8列内容
    print("第1行的内容：", rows0)
    print("第9列的内容", cols8)

    # 获取指定行列的单元格内容
    print("第2行，第9列的内容：", sheet2.cell(1, 8).value)
    print("第2行，第1列的内容：", sheet2.cell_value(1, 0))
    print("第2行，第1列的内容：", sheet2.row(1)[0].value)

    # 获取单元格内容的数据类型
    print(sheet2.cell(1, 0).ctype)
    print(sheet2.cell(3, 9).ctype)


if __name__ == '__main__':
    read_excel()
