import os
from base.mTestCase import MyTestCase
from base.mPageObject import PageObjects

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Add2Cart(MyTestCase):
    """
    添加商品到购物车
    """
    @classmethod
    def setUpClass(cls):
        super(Add2Cart, cls).setUpClass()  # 继承父类的构造方法

    def testAdd2Cart(self):
        """
        driver:继承父类driver
        path：自己提供，测试用例管理文件
        sheetName:excel中的sheet名称
        """
        page = PageObjects(driver=self.driver, path=PATH("../excel/cases.xls"), sheetName="加入购物车")
        result = page.execCase()  # 解析Excel中的用例
        self.assertTrue(result)


    @classmethod
    def tearDownClass(cls):
        super(Add2Cart, cls).tearDownClass()

class OpenCart(MyTestCase):
    """
    添加商品到购物车
    """
    @classmethod
    def setUpClass(cls):
        super(OpenCart, cls).setUpClass()  # 继承父类的构造方法

    def testOpenCart(self):
        """
        driver:继承父类driver
        path：自己提供，测试用例管理文件
        sheetName:excel中的sheet名称
        """
        page = PageObjects(driver=self.driver, path=PATH("../excel/cases.xls"), sheetName="打开购物车")
        result = page.execCase()  # 解析Excel中的用例
        self.assertTrue(result)


    @classmethod
    def tearDownClass(cls):
        super(OpenCart, cls).tearDownClass()
