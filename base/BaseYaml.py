import yaml

def loadYaml(path):
    print("loadYaml:",path)
    try:
        with open(path, encoding='utf-8') as f:
            file_content = yaml.load(f)
            return file_content
    except FileNotFoundError:
        print(u"找不到文件")


if __name__ == '__main__':
    import os
    # PATH = lambda p: os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), p)
    # )
    # t = loadYaml(PATH("../case01.yaml"))
    t = loadYaml("../cases/case01.yaml")
    print(t)




