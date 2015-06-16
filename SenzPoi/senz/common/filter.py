# -*- coidng:utf-8 -*-
__author__ = 'wuzhifan'

from abc import *

from SenzPoi.senz.exceptions import *


class FilterBase(object):
    '''Abstract filter for requests data collections.

    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    @classmethod
    def filter(cls, dataCollection):

        raise NotImplemented(functionName='filter')


"""
class PoiFilter(FilterBase):
    @classmethod
    def filter(cls, dataCollection, poiFunctions):
        ''' Filter or pre-handle data in request here.

        Beacon data in old request format will be dropped here until process method added

        :param dataCollection: contain all
        :return:
        '''
        rowData = {}
        for func in poiFunctions:
            argNames = poiFunctions[func]
            for argName in argNames:
            if type in dataCollection:
                rowData[type] = dataCollection.get(type)
                del dataCollection[type]
"""