# coding=utf-8
import time
import unittest
import logging

from airtest.core.api import *
from Base.BaseSetting import *
from Base.airtestlib import only_connect_devices
from Base.baseview import PocoProject


class startEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = PocoProject()
        logging.info("====setup====")
        # only_connect_devices(__file__, devices=wifi_devices_id)
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        # script content
        print("startapp:{}".format(app_name))
        start_app(app_name)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop_app(app_name)


if __name__ == '__main__':
    unittest.main()
