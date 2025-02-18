# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/19 15:05
# @Author  : 陈强
# @File    : base view.py
# @Software: PyCharm
# @Desc    : 核心方法封装


from airtest.core.api import *
from poco.exceptions import *
import time
from Base.airtestlib import *
import logging
from Base.BaseSetting import *


class PocoProject(object):
    def __init__(self, devices=usb_devices_id):
        """
        初始化函数
        :param devices: 设备标识字符串，可以是WiFi设备标识或USB设备标识，默认为空字符串
        """
        self.dev = None  # 初始化设备变量
        self.devices = devices  # 保存传入的设备标识
        logger = logging.getLogger("airtest")  # 获取名为"airtest"的日志记录器
        logger.setLevel(logging.INFO)  # 设置日志级别 INFO&ERROR
        self.default_timeout = 50  # 默认超时时间设置为50秒
        # 根据传入的设备标识，选择不同的连接方式
        if self.devices == wifi_devices_id:
            print("Connecting via WiFi...")
            only_connect_devices(__file__, devices=wifi_devices_id)  # 仅通过WiFi连接设备
        elif self.devices == usb_devices_id:
            print("Connecting via USB cable...")
            only_connect_devices(__file__, devices=usb_devices_id)  # 仅通过USB连接设备
        else:
            print("Invalid device type provided.")  # 提供的设备类型无效

        # 导入Android UI自动化驱动，并初始化Poco对象
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # 上述Poco对象用于后续的UI自动化操作，配置为使用Airtest输入和不每次动作都截屏

    def wait_for_poco_element(self, element, timeout=None):
        """
        等待元素出现
        :param element: 元素属性
        :param timeout: 过期时间（秒），默认为None（使用默认超时时间）
        :return: 元素
        """
        # 参数校验
        if timeout is not None and timeout < 0:
            raise ValueError("timeout cannot be negative")

        if timeout is None:
            timeout = self.default_timeout  # 使用默认超时时间

        start_time = time.time()
        polling_interval = 0.1  # 初始轮询间隔
        max_polling_interval = 5  # 最大轮询间隔
        while True:
            try:
                if element.exists():  # 检查对象是否存在
                    return element
            except Exception as e:
                # 日志记录异常，以便于问题追踪
                print(f"An error occurred while checking for the element: {e}")
                # 继续等待，而不是直接失败
                pass

            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > timeout:
                raise PocoTargetTimeout('appearance', self)  # 超时异常

            # 使用指数退避策略，增加轮询间隔，避免高CPU占用
            next_polling_interval = min(polling_interval * 2, max_polling_interval)
            time.sleep(next_polling_interval)
            polling_interval = next_polling_interval

    # 示例用法

    def app_poco_write_text(self, element, text, timeout=None):
        """
        在元素出现后向文本框中写入内容（App 端）
        :param element: 元素属性
        :param text: 要写入的文本内容
        :param timeout: 过期时间（秒），默认为 None（使用默认超时时间）
        """
        element = self.wait_for_poco_element(element, timeout)  # 等待元素出现
        element.set_text(text)  # 向文本框中写入内容

    def app_poco_click(self, element, timeout=None):
        """
        在元素出现后点击元素（App 端）
        :param element: 元素属性
        :param timeout: 过期时间（秒），默认为 None（使用默认超时时间）
        """
        element = self.wait_for_poco_element(element, timeout)  # 等待元素出现
        element.click()  # 点击元素

    def app_poco_clear_text(self, element, timeout=None):
        """
        在元素出现后清除文本框内容（App 端）
        :param element: 元素属性
        :param timeout: 过期时间（秒），默认为 None（使用默认超时时间）
        """
        element = self.wait_for_poco_element(element, timeout)  # 等待元素出现
        element.clear_text()  # 清除文本框内容

    def wait_for_element_disappearance(self, element, timeout=None):
        """
        等待元素消失
        :param element: 要等待消失的元素
        :param timeout: 过期时间（秒），默认为None（使用默认超时时间）
        :return: None
        """
        if timeout is None:
            timeout = self.default_timeout  # 使用默认超时时间
        start_time = time.time()
        while True:
            if not element.exists():  # 判断元素是否存在
                return  # 元素不存在，退出循环
            if not element.visible():  # 判断元素是否可见
                return  # 元素不可见，退出循环
            if time.time() - start_time > timeout:
                raise PocoTargetTimeout('disappearance', self)  # 抛出自定义的超时异常
            self.poco.sleep_for_polling_interval()  # 暂停一段时间，等待下一次轮询

    def wait_for_elements_all(self, elements, timeout=None):
        """
        等待所有元素出现再执行，少一个都会报错
        :param elements: 元素集合列表
        :param timeout:超时时间
        :return:
        """
        if not isinstance(elements, tuple):
            raise ValueError('Elements must be a tuple')  # 抛出类型错误异常
        if timeout is None:
            timeout = self.default_timeout  # 使用默认超时时间
        start = time.time()
        while True:
            all_exist = True
            for obj in elements:
                if not obj.exists():
                    all_exist = False
                    break
            if all_exist:
                return elements
            if time.time() - start > timeout:
                raise PocoTargetTimeout('all to appear', elements)
            self.poco.sleep_for_polling_interval()

    def swipe(self, direction, start_point=None, end_point=None):
        """

        :param direction:  滑动方向
        :param start_point: 起始值
        :param end_point: 结束值
        :return:
        """
        # 获取屏幕宽度和高度
        screen_width, screen_height = self.poco.get_screen_size()
        # 如果没有指定起始点或者指定的起始点不在屏幕内，则将其设置为屏幕中心点
        if not start_point or not (0 <= start_point[0] <= screen_width and 0 <= start_point[1] <= screen_height):
            start_point = (screen_width / 2, screen_height / 2)
            if not (0 <= start_point[0] <= screen_width and 0 <= start_point[1] <= screen_height):
                # 如果仍然不在屏幕内，则抛出异常
                raise ValueError("Invalid start_point. The start point is out of screen bounds.")
        # 将起始点坐标转换为相对于屏幕宽度和高度的比例值
        relative_start_point = (start_point[0] / screen_width, start_point[1] / screen_height)
        # 如果没有指定结束点，则根据指定的方向和位移计算出结束点坐标
        if not end_point:
            if direction == 'up':
                end_point = (relative_start_point[0], max(0, relative_start_point[1] - 0.3))
            elif direction == 'down':
                end_point = (relative_start_point[0], min(1, relative_start_point[1] + 0.3))
            elif direction == 'left':
                end_point = (max(0, relative_start_point[0] - 0.3), relative_start_point[1])
            elif direction == 'right':
                end_point = (min(1, relative_start_point[0] + 0.3), relative_start_point[1])
        # 检查结束点坐标是否在屏幕内
        if not (0 <= end_point[0] <= 1 and 0 <= end_point[1] <= 1):
            raise ValueError("Invalid end_point. The calculated end point is out of screen bounds.")
        # 将结束点坐标转换为相对于屏幕宽度和高度的比例值
        relative_end_point = (end_point[0], end_point[1])
        # 调用 Poco 库的 swipe() 方法进行滑动操作，其中 duration 参数指定了滑动的时间（单位：秒）
        self.poco.swipe(relative_start_point, relative_end_point, duration=1)

    def get_element_content(self, element, property_name):
        """
        获取元素的指定属性值
        :param element: 元素对象
        :param property_name: 属性名，如 'text', 'name', 'size' 等
        :return: 元素属性的值，如果获取失败则返回 None
        """
        try:
            if property_name == 'text':
                return element.get_text()
            elif property_name == 'name':
                return element.get("name")
            else:
                return getattr(element, property_name, None)
        except Exception as e:
            print(f"获取元素属性 '{property_name}' 失败：{e}")
            return property_name

    @staticmethod
    def start_app(pakgname):
        """
        启动app
        :param pakgname: 应用包名
        :return:
        """
        start_app(pakgname)

    @staticmethod
    def stop_app(pakgname):
        """
        停止app
        :param pakgname: 应用包名
        :return:
        """
        stop_app(pakgname)

    def video_start_recording(self, max_time, output, orientation):
        """开始录制视频"""
        self.dev = device()
        self.dev.start_recording(max_time=max_time, output=output, orientation=orientation)

    def video_stop_recording(self):
        """结束录制视频"""
        self.dev.stop_recording()


if __name__ == '__main__':
    pass
