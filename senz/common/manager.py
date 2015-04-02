__author__ = 'wuzhifan'

import threadpool

from senz.common.openstack.threadgroup import ThreadGroup
from senz.exceptions import *

INIT_THREAD_NUM = 256
DEFAULT_THREAD_TYPE = 'threading'

class ManagerBase(object):
    pass

class MultiThreadManager(ManagerBase):
    def __init__(self, threadType=DEFAULT_THREAD_TYPE, initThreadNum=INIT_THREAD_NUM):
        self._threadType = threadType
        if threadType == 'threading':
            self.threadPool = threadpool.ThreadPool(initThreadNum)
        elif threadType == 'greenthread':
            self.threadPool = ThreadGroup(initThreadNum)
        else:
            self.threadPool = None
            raise SenzExcption(msg='Unkown thread type!')

    def addThread(self, callback, *args, **kwargs):
        if self._threadType == 'threading':
            requestArgs = [(args, kwargs)]
            requests = threadpool.makeRequests(callback, requestArgs)
            [self.threadPool.putRequest(request) for request in requests]
        elif self._threadType == 'greenthread':
            self.threadPool.add_thread(callback, *args, **kwargs)

