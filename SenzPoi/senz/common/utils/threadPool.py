# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import threading

class WorkThread(threading.Thread):
    pass

class ThreadPool(object):
    def __init__(self, size):
        self.workers = []

    def createWorkers(self, size):
        pass