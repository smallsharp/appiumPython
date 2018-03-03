# coding=utf-8

def printArgs(**kwargs):
    print(kwargs["test"])
    print(kwargs["test1"])
    print(kwargs["test2"])
    print(kwargs.get("test3", "what"))  # 不会报错，返回none
    # print(kwargs["test3"]) # key没有的情况会报错


def test():
    a = ["hello", "python"]
    if "hello" in ["hello", "python"]:
        print("ok")


def testEnd():
    a = ""
    b = ""
    if a=="" and b=="":
        print("0:", a and b)
    else:
        print("1:", a and b)


if __name__ == '__main__':
    # printArgs(test="hello",test1="world",test2="java")
    testEnd()
