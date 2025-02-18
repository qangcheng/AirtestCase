# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/3 13:15
# @Author  : 陈强
# @File    : BaseSetting.py
# @Software: PyCharm
# @Desc    :
import os

BaseDIR = os.path.dirname(os.path.dirname(__file__))
LogDIR = os.path.join(BaseDIR, "logs\\")
locaReportDIR = os.path.join(BaseDIR, "report\\")
TestDataDIR = os.path.join(BaseDIR, "TestData")
PictureDIR = os.path.join(TestDataDIR, "picture\\")
EntranceDIR = os.path.join(BaseDIR, "Entrance\\")
staticDIR = os.path.join(EntranceDIR, "static\\")
ReportDIR = os.path.join(staticDIR, "Report\\")
usb_devices_id = ["android://127.0.0.1:5037/R58M93NAP7D?touch_method=MAXTOUCH&", ]
wifi_devices_id = ["Android://127.0.0.1:5037/1192.168.1.26:7788"]
app_name = "com.gitread"
USERNAME = "test"
PD = "123456"

import socket


def get_local_ip():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip地址
    ip = socket.gethostbyname(hostname)
    ip_port = "http://" + ip + ":5000/"
    # print(ip_port)
    ip_port_Report_DIR = ip_port + "static/Report/"
    return ip_port_Report_DIR


# 万能装饰器

def outer(func):
    def inner(*args, **kwargs):
        arg = func(*args, **kwargs)
        return arg

    return inner


# 三层闭包 本质就是为了接受参数
def get_parameter(*args, **kwargs):
    def outer(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return outer


if __name__ == '__main__':
    pass
    print(staticDIR)
    print(ReportDIR)
    print(locaReportDIR)
    # print(BaseDIR)
    # print(LogDIR)
    # print(ReportDIR)
    # print(PictureDIR)
