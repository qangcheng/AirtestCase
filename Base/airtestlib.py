# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/25 9:26
# @Author  : 陈强
# @File    : airtestlib.py
# @Software: PyCharm
# @Desc    : 源码重写

import os
import shutil
from airtest.core.helper import G
from airtest.core.settings import Settings as ST


def only_connect_devices(basedir=None, devices=None, project_root=None, compress=None):
    """
    连接指定设备到项目中。

    :param basedir: 基础目录路径，如果提供，会将其添加到全局基础目录列表中。
    :param devices: 要连接的设备列表，每个设备通过其URI标识。
    :param project_root: 项目的根目录，用于设置项目的基础路径。
    :param compress: 截图图像的压缩率，整数，范围在[1, 99]之间，默认为10。

    :return: 如果指定了设备列表并成功连接了设备，则返回连接上的第一个设备的句柄；否则不返回任何内容。
    """
    # 处理basedir参数，将其添加到全局基础目录列表中
    if basedir:
        if os.path.isfile(basedir):  # 如果basedir是一个文件，则将其目录加入到全局目录列表
            basedir = os.path.dirname(basedir)
        if basedir not in G.BASEDIR:  # 避免重复添加
            G.BASEDIR.append(basedir)

    # 连接指定的设备
    if devices:
        for dev in devices:
            from airtest.core.api import connect_device  # 动态导入connect_device函数
            Dev = connect_device(dev)  # 连接设备并返回设备对象
            return Dev  # 仅连接第一个设备后即返回

    # 设置项目根目录
    if project_root:
        ST.PROJECT_ROOT = project_root

    # 设置截图压缩率
    if compress:
        ST.SNAPSHOT_QUALITY = compress


def only_set_logdir(logdir):
    """
    设置并确保日志目录存在。
    参数:
    logdir (str): 指定的日志目录路径。
    返回:
    无
    """
    if os.path.exists(logdir):
        shutil.rmtree(logdir)  # 如果日志目录已存在，则删除该目录
    os.makedirs(logdir, exist_ok=True)  # 创建日志目录，如果目录已存在则不抛出异常
    ST.LOG_DIR = logdir  # 更新全局日志目录变量
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))  # 设置日志文件路径


if __name__ == '__main__':
    pass
