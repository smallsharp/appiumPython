import sys
import os
from base.BaseTestCase import MyTestCase
from excel._PageObjects import PageObjects

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# 测试用例类,继承MyTestCase
class Login(MyTestCase):

    @classmethod
    def setUpClass(cls):
        super(Login, cls).setUpClass()  # 继承父类的构造方法

    def testLogin(self):
        """
        driver:继承父类driver
        path：自己提供，测试用例管理文件
        sheetName:excel中的sheet名称
        """
        loginPage = PageObjects(driver=self.driver, path=PATH("../excel/cases.xls"), sheetName="登录")
        loginPage.parse_case()  # 解析Excel中的用例

        # 放到这里，会接着执行
        # logout = PageObjects(driver=self.driver,path=PATH("../excel/cases.xls"),sheetName="退出登录")
        # logout.parse_case()
        # loginPage.checkPoint(caseName=sys._getframe().f_code.co_name, logger=self.logger, devices=self.devicesName)
        # loginPage.check()

    # 放在这里，也是会接着执行，因为当前是setUpClass，不是setUp
    # def testLogout(self):
    #     logout = PageObjects(driver=self.driver,path=PATH("../excel/cases.xls"),sheetName="退出登录")
    #     logout.parse_case()

    @classmethod
    def tearDownClass(cls):
        super(Login, cls).tearDownClass()


class Logout(MyTestCase):

    @classmethod
    def setUpClass(cls):
        super(Logout,cls).setUpClass()

    def testLogout(self):
        logout = PageObjects(driver=self.driver,path=PATH("../excel/cases.xls"),sheetName="退出登录")
        logout.parse_case()

    @classmethod
    def tearDownClass(cls):
        super(Logout,cls).tearDownClass()

