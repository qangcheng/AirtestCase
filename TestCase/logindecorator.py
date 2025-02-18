# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 15:57
# @Author  : 陈强
# @File    : FindPage.py
# @Software: PyCharm

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
from Base.airtestlib import *
import logging
from Base.BaseSetting import *


def get_parameter(logname):
    def outer(func):
        def inner(*args, **kwargs):
            only_set_logdir(LogDIR + logname)
            try:
                arg = func(*args, **kwargs)
            except Exception as e:
                log(e, desc="测试信息", snapshot=True)
                raise e
            finally:
                simple_report(__file__, logpath=LogDIR + logname,output=ReportDIR + logname + ".html")
            return arg
        return inner
    return outer


class LogIn(object):
    def __init__(self, pakgname):
        """
        初始化操作连接手机
        """
        logger = logging.getLogger("airtest")
        logger.setLevel(logging.ERROR)
        if not cli_setup():
            only_connect_devices(devices=["android://127.0.0.1:5037/R28M50ZP1EP?touch_method=MAXTOUCH&",])
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # script content
        print("start...")
        start_app(pakgname)

    def __del__(self):
        print("end")

    def Close_App(self, pakgname):
        stop_app(pakgname)

    @get_parameter("login")
    def admin_login(self, user, password):
        """
                suki包登录测试
        """
        input_user = self.poco("com.gitread:id/idEt")
        input_user.set_text(user)
        input_psd = self.poco("com.gitread:id/passwordEt")
        input_psd.set_text(password)
        self.poco.device.snapshot("screenshot.png")  # 截图
        self.poco("com.gitread:id/continueTv").click()
        sleep(2)
        # assert_exists(Template(r"tpl1701330238432.png", record_pos=(-0.003, 0.846), resolution=(1080, 2340)),
        #             "登录完成，进入live页面")
        assert_exists(
            Template(PictureDIR + "tpl1701414161609.png", record_pos=(0.019, 1.019), resolution=(1080, 2340)),
            "登录成功")
        keyevent(home)


if __name__ == '__main__':
    login = LogIn("com.gitread")
    login.admin_login("61982065", "123456")
    login.Close_App("com.gitread")
