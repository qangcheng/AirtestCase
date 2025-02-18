# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/9 16:42
# @Author  : 陈强
# @File    : TestLogin.py
# @Software: PyCharm
# @Desc    :

"""
TestLogin.py
"""

import unittest
from airtest.report.report import simple_report
from page.login import Login
from Base.baseview import *
from TestSuite.myunit import startEnd


def get_parameter(Logname,  casedesc="描述信息"):
    def outer(func):
        def inner(self, *args, **kwargs):
            only_set_logdir(LogDIR + Logname)
            self.__dict__['_testMethodDoc'] = casedesc
            self.__dict__['_start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            try:
                arg = func(self, *args, **kwargs)
            except Exception as e:
                log(e, desc="测试信息", snapshot=True)
                raise e
            finally:
                simple_report(__file__, logpath=LogDIR + Logname,
                              output=ReportDIR + Logname + ".html")  # we服务报告地址
                simple_report(__file__, logpath=LogDIR + Logname,
                              output=locaReportDIR + Logname + ".html")  # 本地报告生成地址
                self.__dict__['_html_path'] = ReportDIR + Logname + ".html"    # 本地生成报告
                self.__dict__['_html_path'] = get_local_ip() + Logname + ".html"  # 服务器生成报告地址
            return arg
        return inner
    return outer


class TestLogin(startEnd):
    """
    登录测试
    """
    def setUp(self):
        self.s = Login()

    @get_parameter("Login_success", "登录成功用例")
    def test_login_success(self):
        """
        测试登录成功
        """
        self.p.video_start_recording(max_time=1800, output=LogDIR +"Login_success", orientation=1)
        self.s.user_login("61982065", "123456")
        # self.p.poco(assert_exists(
        #     Template(PictureDIR + r"tpl1705386626970.png", record_pos=(0.055, 0.854), resolution=(1080, 2340)),
        #     "登录成功"))
        try:
            # self.p.app_poco_click(self.s.close_button)
            # self.s.click_later()
            follow_name = self.p.get_element_content(self.p.poco(text="Follow"), "text")
            print(follow_name)
            assert_equal("Follow", follow_name, "已进入首页")
        except Exception as e:
            log(e, desc="Home page failure, reported the reason for the error:{}".format(e), snapshot=True)
        self.p.video_stop_recording()

    @get_parameter("logout_success", "登出成功用例")
    def test_logout_success(self):

        self.p.video_start_recording(max_time=1800, output=LogDIR + "logout_success", orientation=1)
        self.s.user_logout()
        try:
            self.p.poco("com.gitread:id/idEt")
            assert_exists(Template(PictureDIR+r"tpl1708335447807.png", record_pos=(0.026, -0.229), resolution=(1080, 2340)), "登出成功")
        except Exception as e:
            log(e, desc=":Log out error Please check log:{}".format(e), snapshot=True)
        self.p.video_stop_recording()


if __name__ == '__main__':
    unittest.main()








