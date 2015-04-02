# -*- coding: utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.manager import ManagerBase, MultiThreadManager



class PoiManager(MultiThreadManager):
    def __init__(self):
        super(PoiManager, self).__init__()

    def parseFromGps(self, gpsList):
        pass


class PoiGroupManager(ManagerBase):
    pass

