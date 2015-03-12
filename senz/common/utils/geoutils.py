__author__ = 'lsg'

from math import *

def distance(lon1, lat1, lon2, lat2):
        """
        calulate distence from GPS
        :param lon1:
        :param lat1:
        :param lon2:
        :param lat2:
        :return:
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return 6371300 * c
