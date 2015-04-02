# -*- coidng:utf-8 -*-
__author__ = 'wuzhifan'

from abc import *

from senz.exceptions import *


class FilterBase(object):
    '''Abstract filter for requests data collections.

    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    @classmethod
    def filter(cls, dataCollection):

        raise NotImplemented(functionName='filter')
