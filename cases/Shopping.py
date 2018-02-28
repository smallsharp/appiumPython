import sys
import os
from base.BaseTestCase import MyTestCase
from excel._PageObjects import PageObjects

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class AddToCart(MyTestCase):
    """
    添加商品到购物车
    """
    @classmethod
    def setUpClass(cls):
        super(AddToCart, cls).setUpClass()  # 继承父类的构造方法

    def testLogin(self):
        """
        driver:继承父类driver
        path：自己提供，测试用例管理文件
        sheetName:excel中的sheet名称
        """
        page = PageObjects(driver=self.driver, path=PATH("../excel/cases.xls"), sheetName="加入购物车")
        page.parse_case()  # 解析Excel中的用例

    @classmethod
    def tearDownClass(cls):
        super(AddToCart, cls).tearDownClass()
