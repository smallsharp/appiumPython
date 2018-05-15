import os

def getOnlineDevices():
    """
    获取当前连接的设备
    :return:设备列表
    """
    res = os.popen("adb devices").readlines()  # ['List of devices attached\n', 'GWY0217826005102\tdevice\n', '\n']
    devices = []
    for i in res:
        if len(i) > 5 and "devices" not in i:
            devices.append(i.split()[0])
    if not devices:
        raise Exception("No Devices Found!")  # 没有找到设备
    return devices


class AppiumConfig:

    # 85GBBMA2353T
    @classmethod
    def init(cls):
        """
        初始化设备列表的基本配置
        :return: 如 [{'deviceName': 'LE67A06310143950', 'port': '4723', 'bport': '9515'}]
        """
        deviceNameList = getOnlineDevices()
        if len(deviceNameList) > 0:
            config = []
            port = 4723
            for name in deviceNameList:
                simpleConfig = {}
                simpleConfig["deviceName"] = name
                simpleConfig["port"] = str(port)  # 端口号
                simpleConfig["bport"] = str(port + 4792)  # bootstrap 端口号
                simpleConfig["ip"] = "127.0.0.1"
                port += 2
                config.append(simpleConfig)
            return config


if __name__ == '__main__':
    AppiumConfig.init()
