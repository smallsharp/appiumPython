import xlsxwriter

from datetime import datetime
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

'''
统计数据相关
'''

'''
result bool
logger 记录日志类 class
driver
testinfo

'''


def countInfo(**kwargs):
#     get_phone = getPhoneInfo(kwargs["devices"])
#     phone_name = get_phone["brand"] + "_" + get_phone["model"] + "_" + "android" + "_" + get_phone["release"]
#     _info = {}
#     step = ""  # 操作步骤信息
#     check_step = ""  # 检查点步骤信息
# 
#     for case in kwargs["testCase"]:
#         step = step + case["info"] + "\n"
# 
#     if type(kwargs["testCheck"]) == list:  # 检查点为列表
#         for check in kwargs["testCheck"]:
#             check_step = check_step + check["info"] + "\n"
#     elif type(kwargs["testCheck"]) == dict:
#         check_step = kwargs["testCheck"]["info"]
#     else:
#         print("获取检查点步骤数据错误，请检查")
#         print(kwargs["testCheck"])
# 
#     _info["step"] = step  # 用例操作步骤
#     _info["checkStep"] = check_step  # 用例检查点
# 
#     if kwargs["result"]:
#         _info["result"] = "通过"
#     else:
#         _info["result"] = "失败"  # 用例接开关
#         _info["img"] = kwargs["logger"].checkPointNG(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
#                                                       checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
#                                                           "msg", "none"))
#     _info["id"] = kwargs["testInfo"][0]["id"]  # 用例id
#     _info["title"] = kwargs["testInfo"][0]["title"]  # 用例名称
#     _info["caseName"] = kwargs["caseName"]  # 测试函数
#     _info["phoneName"] = phone_name  # 手机名
#     _info["msg"] = kwargs["testInfo"][0].get("msg", "")  # 备注
#     _info["info"] = kwargs["testInfo"][0]["info"]  # 前置条件
# 
#     writeInfo(data=_info, path=PATH("../Log/info.pickle"))
#     # print(read(PATH("../Log/info.pickle")))
    pass


def countSum(result):
#     data = {"sum": 0, "pass": 0, "fail": 0}
#     _read = read(PATH("../Log/sum.pickle"))
#     if _read:
#         data = _read
#     data["sum"] = data["sum"] + 1
#     if result:
#         data["pass"] = data["pass"] + 1
#     else:
#         data["fail"] = data["fail"] + 1
#     write(data=data, path=PATH("../Log/sum.pickle"))
#     print(read(PATH("../Log/sum.pickle")))
    pass


def write_reconnect(msg, path=""):
#     write(msg, path=path)
    pass
    # print(read_reconnect(path))


def countDate(testDate, testSumDate):
#     print("--------- countDate------")
#     data = read(PATH("../Log/sum.pickle"))
#     print(data)
#     if data:
#         data["testDate"] = testDate
#         data["testSumDate"] = testSumDate
#         write(data=data, path=PATH("../Log/sum.pickle"))
#     else:
#         print("统计数据失败")
    pass


def writeExcel():
#     workbook = xlsxwriter.Workbook(PATH('../Report/Report.xlsx'))
#     worksheet = workbook.add_worksheet("测试总况")
#     worksheet2 = workbook.add_worksheet("测试详情")
#     operateReport = OperateReport(workbook)
#     operateReport.init(worksheet, read(PATH("../Log/sum.pickle")))
#     operateReport.detail(worksheet2, readInfo(PATH("../Log/info.pickle")))
#     operateReport.close()
# 
#     destroy()  # 删除文件
    pass


