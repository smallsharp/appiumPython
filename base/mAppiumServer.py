# -*- coding: utf-8 -*-
import os
import urllib.request
from urllib.error import URLError
from multiprocessing import Process
import time
import platform
import subprocess
import threading

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Server:

    def __init__(self, devList=None):
        self.devList = devList

    def start(self):
        """start the appium server
        # appium -a 127.0.0.1 -p 4723 -bp 9515 -U LE67A06310143950 --session-override
        # appium -a 127.0.0.1 -p 4725 -bp 9517 -U 85GBBMA2353T --session-override
        """
        for i in range(0, len(self.devList)):
            print("-" * 50)
            ip = self.devList[i]["ip"]
            port = self.devList[i]["port"]
            bport = self.devList[i]["bport"]
            device = self.devList[i]["deviceName"]
            # cmd = "appium -a %s -p %s -bp %s -U %s" % (ip, port, bport, deviceName + " --session-override " + ">" + deviceName + ".log")
            cmd = "appium -a {} -p {} -bp {} -U {} --session-override>{}.log" \
                .format(ip, port, bport, device, device)
            print("cmd:", cmd)
            if platform.system() == "Windows":  # windows下启动server
                thread = RunCommand(cmd)
                p = Process(target=thread.start())
                p.start()
                print("starting server now, wait seconds...")
                while True:
                    # http://127.0.0.1:4723/wd/hub/status
                    if self.isRunning("http://" + ip + ":" + port + "/wd/hub" + "/status"):
                        print("congratulations,server is started...")
                        print("--" * 50)
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
        response = None
        time.sleep(1)
        try:
            response = urllib.request.urlopen(url, timeout=5)
            if str(response.getcode()).startswith("2"):
                return True
            else:
                return False
        except URLError:
            return False
        finally:
            if response:
                response.close()

    def stop(self, devices):
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe")
        else:
            for device in devices:
                # mac
                cmd = "lsof -i :{0}".format(device["port"])
                plist = os.popen(cmd).readlines()
                plisttmp = plist[1].split("    ")
                plists = plisttmp[1].split(" ")
                # print plists[0]
                os.popen("kill -9 {0}".format(plists[0]))

    def re_start_server(self):
        pass


class RunCommand(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)
