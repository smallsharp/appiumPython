"""
    属性配置
"""
class Attr(object):

    # Excel中的关键数据，对应Excel中的列，具体使用见MyOperation
    ID = 0 # ID
    Prerequisite1 = 1 # 前置条件1
    Prerequisite2 = 2 # 前置条件2
    STEP = 3 # 步骤
    FIND_TYPE = 4  # 查询类型
    ELEMENT_INFO = 5  # 元素ID,XPATH等信息
    ELEMENT_INDEX= 6 # 元素索引
    OPERATE_TYPE = 7  # 操作类型
    DATA = 8  # 测试数据
    CHECK_TYPE = 9 # 断言类型
    CHECK_EXPECT = 10 # 预期的数据

    # 定位元素的方式
    ID = "id"
    XPATH = "xpath"
    CLASS = "class"
    ACCESSIBILITY = "discription"
    TEXT = "text"

    # 操作方式需要和Excel中操作方法下的value保持一致
    CLICK = "click"
    TAP = "tap"
    SWIPE = "swipe"
    SEND_KEYS = "sendkeys"
    PRESS_KEY_CODE = "presskeycode"

    # Excel中的断言类型
    CHECK_PAGE = "检查页面"
    CHECK_ID = "检查ID"
    CHECK_TEXT = "检查文本"

    # 断言页面时，等待页面加载时间
    CHECK_PAGE_TIME= 5