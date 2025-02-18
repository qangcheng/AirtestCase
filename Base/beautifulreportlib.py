# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/30 19:34
# @Author  : 陈强
# @File    : beautifulreportlib.py
# @Software: PyCharm
# @Desc    :
import os
import sys
from functools import wraps
from BeautifulReport.BeautifulReport import ReportTestResult, BeautifulReport
import time
import json
import platform
import base64

HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""


class PATH:
    """ all file PATH meta """
    template_path = os.path.join(os.path.dirname(__file__), 'template')  # BASE 目录下的template
    config_tmp_path = os.path.join(template_path, 'template.html')  # template 目录下的template.html文件


class DIYMakeResultJson(object):
    """
    生成HTML表格标签的类，用于构建测试结果的HTML表格结构。
    """
    def __init__(self, datas: tuple):
        """
        初始化对象

        :param datas: 所有返回数据的元组结构，包括测试结果相关的信息
        """
        self.datas = datas
        self.result_schema = {}  # 初始化测试结果的数据结构

    def __setitem__(self, key, value):
        """
        设置self[key]的值

        :param key: 键值
        :param value: 值
        :return: 无返回值
        """
        self[key] = value

    def __repr__(self) -> str:
        """
        返回对象的HTML结构

        :rtype: str
        :return: 返回一个JSON格式的字符串，表示构造完成的<tr>表单
        """
        keys = (
            'className',
            'methodName',
            'description',
            'html_path',
            'start_time',
            'spendTime',
            'status',
            'log',
        )
        for key, data in zip(keys, self.datas):
            self.result_schema.setdefault(key, data)  # 将测试结果数据填充到result_schema中
        return json.dumps(self.result_schema)  # 返回JSON格式的字符串表示测试结果数据


class DIYReportTestResult(ReportTestResult):
    @staticmethod
    def get_testcase_property(test) -> tuple:
        """
        获取测试用例的属性

        :param test: 测试用例对象
        :return: (class_name, method_name, method_doc, html_path) -> 元组，包含测试用例的相关属性信息
        """
        # 获取测试用例的相关属性
        class_name = test.__class__.__qualname__  # 获取测试类名
        method_name = test.__dict__['_testMethodName']  # 获取测试方法名
        method_doc = test.__dict__['_testMethodDoc']  # 获取测试方法文档字符串
        html_path = test.__dict__['_html_path']  # 获取测试报告的HTML路径
        start_time = test.__dict__['_start_time']  # 获取测试开始时间

        return class_name, method_name, method_doc, html_path, start_time  # 返回包含测试用例属性的元组

    def stopTestRun(self, title=None) -> dict:
        """
        所有测试执行完成后调用的方法，用于生成测试报告的最终结果

        :param title: 报告标题
        :return: 测试报告的字段字典，包含各项统计信息
        """
        # 设置字段值
        self.fields['testPass'] = self.success_counter  # 通过的用例数量

        # 将每个测试结果转换为字典，并添加到 testResult 列表中
        for item in self.result_list:
            item = json.loads(str(DIYMakeResultJson(item)))
            self.fields.get('testResult').append(item)

        self.fields['testAll'] = len(self.result_list)  # 执行用例数量
        self.fields['testName'] = title if title else self.default_report_name  # 测试报告名称
        self.fields['testFail'] = self.failure_count  # 失败的用例数量
        self.fields['beginTime'] = self.begin_time

        # 计算测试执行时间
        end_time = int(time.time())
        start_time = int(time.mktime(time.strptime(self.begin_time, '%Y-%m-%d %H:%M:%S')))
        self.fields['totalTime'] = str(end_time - start_time) + 's'  # 所有测试用例执行的时间

        self.fields['testError'] = self.error_count  # 错误的用例数量
        self.fields['testSkip'] = self.skipped  # 跳过的用例数量

        return self.fields  # 返回测试报告的字段字典


class DIYBeautifulReport(DIYReportTestResult, PATH):
    img_path = 'img/' if platform.system() != 'Windows' else 'img\\'

    def __init__(self, suites):
        super(DIYReportTestResult, self).__init__(suites)
        self.suites = suites
        self.report_dir = None
        self.title = '自动化测试报告'
        self.filename = 'report.html'

    def report(self, description, filename: str = None, report_dir='.', log_path=None, theme='theme_default'):
        """
            生成测试报告,并放在当前运行路径下
        :param report_dir: 生成report的文件存储路径
        :param filename: 生成文件的filename
        :param description: 生成文件的注释
        :param theme: 报告主题名 theme_default theme_cyan theme_candy theme_memories
        :return:
        """
        if log_path:
            import warnings
            message = ('"log_path" is deprecated, please replace with "report_dir"\n'
                       "e.g. result.report(filename='测试报告_demo', description='测试报告', report_dir='report')")
            warnings.warn(message)

        if filename:
            # 防止用户忘记写后缀，给拼接后缀
            self.filename = filename if filename.endswith('.html') else filename + '.html'

        if description:
            self.title = description

        self.report_dir = os.path.abspath(report_dir)  # Beautiful文件目录
        os.makedirs(self.report_dir, exist_ok=True)
        self.suites.run(result=self)
        self.stopTestRun(self.title)
        self.output_report(theme)
        text = '\n测试已全部完成, 可打开 {} 查看报告'.format(os.path.join(self.report_dir, self.filename))
        print(text)

    def output_report(self, theme):
        """
            生成测试报告到指定路径下
        :return:
        """

        def render_template(params: dict, template: str):
            for name, value in params.items():
                name = '${' + name + '}'
                template = template.replace(name, value)
            return template

        template_path = self.config_tmp_path
        # self.template_path 指向base目录下的template下的template.json
        with open(os.path.join(self.template_path, theme + '.json'), 'r') as theme:
            render_params = {
                **json.load(theme),
                'resultData': json.dumps(self.fields, ensure_ascii=False, indent=4)
            }

        override_path = os.path.abspath(self.report_dir) if \
            os.path.abspath(self.report_dir).endswith('/') else \
            os.path.abspath(self.report_dir) + '/'

        with open(template_path, 'rb') as file:
            body = file.read().decode('utf-8')
        with open(override_path + self.filename, 'w', encoding='utf-8', newline='\n') as write_file:
            html = render_template(render_params, body)
            write_file.write(html)

    @staticmethod
    def img2base(img_path: str, file_name: str) -> str:
        """
            接受传递进函数的filename 并找到文件转换为base64格式
        :param img_path: 通过文件名及默认路径找到的img绝对路径
        :param file_name: 用户在装饰器中传递进来的文件匿名
        :return:
        """
        pattern = '/' if platform != 'Windows' else '\\'

        with open(img_path + pattern + file_name, 'rb') as file:
            data = file.read()
        return base64.b64encode(data).decode()

    def add_test_img(*pargs):
        """
            接受若干个图片元素, 并展示在测试报告中
        :param pargs:
        :return:
        """
        def _wrap(func):
            @wraps(func)
            def __wrap(*args, **kwargs):
                img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
                os.makedirs(img_path, exist_ok=True)
                testclasstype = str(type(args[0]))
                # print(testclasstype)
                testclassnm = testclasstype[testclasstype.rindex('.') + 1:-2]
                # print(testclassnm)
                img_nm = testclassnm + '_' + func.__name__
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    if 'save_img' in dir(args[0]):
                        save_img = getattr(args[0], 'save_img')
                        save_img(os.path.join(img_path, img_nm + '.png'))
                        data = BeautifulReport.img2base(img_path, img_nm + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    sys.exit(0)
                print('<br></br>')

                if len(pargs) > 1:
                    for parg in pargs:
                        print(parg + ':')
                        data = BeautifulReport.img2base(img_path, parg + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    return result
                if not os.path.exists(img_path + pargs[0] + '.png'):
                    return result
                data = BeautifulReport.img2base(img_path, pargs[0] + '.png')
                print(HTML_IMG_TEMPLATE.format(data, data))
                return result
            return __wrap
        return _wrap
