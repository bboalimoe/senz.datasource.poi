# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.manager import ManagerBase

class ActivityManager(ManagerBase):
    def __init__(self):
        super(ActivityManager, self).__init__()

    def activity_mapping(self, context, gps, user_id):
        pass