# -*- coding: utf-8 -*-
import os
import urllib.request
from multiprocessing import Process
import time
import platform
import subprocess
import threading

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class AppiumServer:

    def __init__(self, devices):
        self.devices = devices

    def start(self):
        """
        start server
        cmd:appium -a 127.0.0.1 -p 4723 -bp 9515 -U LE67A06310143950 --session-override
        :return: server
        """
        for i in range(0, len(self.devices)):
            ip = self.devices[i]["ip"]
            port = self.devices[i]["port"]
            bport = self.devices[i]["bport"]
            device = self.devices[i]["deviceName"]
            logPath = PATH('../report/{}'.format(device))
            cmd = "appium -a {} -p {} -bp {} -U {} --session-override>{}.log".format(ip, port, bport, device, logPath)
            print("cmd:", cmd)
            if platform.system() == "Windows":  # windows下启动server
                thread = MyThread(cmd)
                p = Process(target=thread.start())
                p.start() # thread run
                print("starting server now, wait seconds...")
                while True:
                    # http://127.0.0.1:4723/wd/hub/status
                    if self.isRunning("http://" + ip + ":" + port + "/wd/hub" + "/status"):
                        print("congratulations,server is running now...")
                        print("--" * 50)
                        break
            else:
                appium = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                                          close_fds=True)
                while True:
                    appium_line = appium.stdout.readline().strip().decode()
                    time.sleep(1)
                    print("---------start----------")
                    if 'listener started' in appium_line or 'Error: listen' in appium_line:
                        print("----server_ 成功---")
                        break

    def isRunning(self, url):
        """
        check whether the server is running or not
        :param url: url to check
        :return: True or False
        """
        response = None
        time.sleep(1)
        try:
            response = urllib.request.urlopen(url, timeout=5)
            if str(response.getcode())=='200':
                return True
            else:
                return False
        except Exception:
            return False
        finally:
            if response:
                response.close()

    def stop(self, devices):
        """
        stop the server
        :param devices: devices
        :return: kill the server
        """
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe") # 清理node进程
        else:
            for device in devices:
                # mac
                cmd = "lsof -i :{0}".format(device["port"])
                plist = os.popen(cmd).readlines()
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                # print plists[0]
                os.popen("kill -9 {0}".format(plists[0]))

    def restart(self):
        pass


class MyThread(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)
