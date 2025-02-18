# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/5 10:08
# @Author  : 陈强
# @File    : suite_login.py
# @Software: PyCharm
# @Desc    :
import logging
import time
from Base.baseview import PocoProject
from Base.BaseSetting import app_name
from Base.BaseSetting import *


class Login(object):
    def __init__(self):
        self.p = PocoProject()
        # 登录相关元素
        self.user_button = self.p.poco("com.gitread:id/idEt")
        self.prd_button = self.p.poco("com.gitread:id/passwordEt")
        self.login_button = self.p.poco("com.gitread:id/continueTv")
        self.GoogleLogin_button = self.p.poco(text="Sign in with Google")
        self.close_button = self.p.poco("com.gitread:id/liveStartCloseIv")
        self.later_button = self.p.poco("com.gitread:id/tv_later")

        # 登出相关元素
        self.settings_button = self.p.poco(text="Settings")
        self.logout_button = self.p.poco(text="Logout")

    def input_username(self, user_name):
        try:
            self.p.app_poco_write_text(self.user_button, text=user_name)
        except Exception as e:
            print(f"输入用户名时出现异常：{e}")

    def input_psd(self, psd):
        try:
            self.p.app_poco_write_text(self.prd_button, text=psd)
        except Exception as e:
            print(f"输入密码时出现异常：{e}")

    def click_login(self):
        try:
            self.p.app_poco_click(self.login_button)
        except Exception as e:
            print(f"点击登录按钮时出现异常：{e}")

    def click_later(self):
        try:
            self.p.app_poco_click(self.later_button)
        except Exception as e:
            print(f"点击稍后按钮时出现异常：{e}")

    def click_close(self):
        try:
            self.p.app_poco_click(self.close_button)
        except Exception as e:
            print(f"点击关闭按钮时出现异常：{e}")

    def click_me(self):
        try:
            self.p.poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring(
                "android:id/content").offspring("android.view.ViewGroup").child("android.widget.FrameLayout")[
                4].offspring("com.gitread:id/icon").click()
        except Exception as e:
            print(f"点击我的按钮时出现异常：{e}")

    def click_settings(self):
        try:
            self.p.app_poco_click(self.settings_button)
        except Exception as e:
            print(f"点击设置按钮时出现异常：{e}")

    def click_logout(self):
        try:
            self.p.app_poco_click(self.logout_button)
        except Exception as e:
            print(f"点击退出按钮时出现异常：{e}")

    def user_login(self, username, psd):
        try:
            self.input_username(username)
            self.input_psd(psd)
            self.click_login()
            self.click_close()
            if self.later_button:
                self.click_later()
            else:
                self.p.poco(text="Follow").click()
        except Exception as e:
            print(f"用户登录过程中出现异常：{e}")

    def user_logout(self):
        try:
            self.click_me()
            self.p.swipe("up")
            time.sleep(1)
            self.click_settings()
            self.click_logout()
        except Exception as e:
            print(f"用户登出过程中出现异常：{e}")


if __name__ == '__main__':
    try:
        s = PocoProject()
        a = Login()
        print(f"start: {app_name}")
        a.p.start_app("com.gitread")
        a.user_login("61982065", "123456")
        a.user_logout()
    except Exception as e:
        print(f"程序运行出现异常：{e}")
