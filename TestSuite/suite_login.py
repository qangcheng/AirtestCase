# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/4 18:21
# @Author  : 陈强
# @File    : suite_login.py
# @Software: PyCharm
# @Desc    :

import unittest
from Base.beautifulreportlib import DIYBeautifulReport
from TestCase import TestLogin
from BeautifulReport import BeautifulReport
from Base.BaseSetting import LogDIR, staticDIR, ReportDIR

# 创建一个测试套件
suite = unittest.TestSuite()

# 加载TestLogin模块中的测试用例，并添加到测试套件中
TestCases = unittest.TestLoader().loadTestsFromModule(TestLogin)
suite.addTest(TestCases)

# 创建一个文本测试运行器，执行测试套件，并在控制台输出测试结果
# runner = unittest.TextTestRunner()

# 使用BeautifulReport生成测试报告
# runner = BeautifulReport(suite)
runner = DIYBeautifulReport(suite)
runner.report(report_dir=ReportDIR, description="suki测试用例", filename="SukiTestReport.html")
