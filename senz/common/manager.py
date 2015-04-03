# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.openstack.threadgroup import ThreadGroup
from senz.exceptions import *

'''threading pool methods.

These may be overwrite if threading pool is changed.
'''
THREADING_POOL_MODULE_NAME = 'threadpool'
threading_pool_module = __import__(THREADING_POOL_MODULE_NAME)

def threading_pool_init(init_size):
    return threading_pool_module.ThreadPool(init_size)

def threading_pool_add_thread(pool, callback, *args, **kwargs):
    request_args = [(args, kwargs)]
    requests = threading_pool_module.makeRequests(callback, request_args)
    [pool.putRequest(request) for request in requests]



'''Poi-senz managers base.
'''
INIT_THREAD_NUM = 256
DEFAULT_THREAD_TYPE = 'threading'   #'greenthread' type has some problem with current request lib

class ManagerBase(object):
    pass

class MultiThreadManager(ManagerBase):
    '''Manager with thread pool to handle request.

    '''
    def __init__(self, thread_type=DEFAULT_THREAD_TYPE, init_size=INIT_THREAD_NUM):
        self._thread_type = thread_type
        if thread_type == 'threading':
            self.thread_pool = threading_pool_init(init_size)
        elif thread_type == 'greenthread':
            self.thread_pool = ThreadGroup(init_size)
        else:
            self.thread_pool = None
            raise SenzExcption(msg='Unkown thread type!')

    def add_thread(self, callback, *args, **kwargs):
        if self._thread_type == 'threading':
            threading_pool_add_thread(self.thread_pool, callback, *args, **kwargs)
        elif self._thread_type == 'greenthread':
            self.thread_pool.add_thread(callback, *args, **kwargs)

    def wait(self):
        if self.thread_pool:
            self.thread_pool.wait()

