
import os


if __name__ == '__main__':


    # print (os.path.dirname(os.path.abspath("__file__")))
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    # 当前文件所在路径
    path1 = os.path.dirname(__file__)
    print(path1)

    # 拼接两个路径
    path2 = os.path.join(os.path.join(os.path.dirname(__file__),"log"))
    print(path2)

    # 拼接路径后，获取其绝对路径
    path3 = os.path.abspath(path2)
    print(path3)

    # 注意对比和上个的区别
    print(PATH("../log"))

    print(1 == '2')
