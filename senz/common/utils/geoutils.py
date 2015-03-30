__author__ = 'lsg'

from math import *

class LocationAndTime(object):
    """Data including place and record time"""

    def __init__(self, _time, _latitude, _longitude):
        self.time = _time
        self.latitude = _latitude
        self.longitude = _longitude

    def time(self):
        return self.time

    def latitude(self):
        return self.latitude

    def longitude(self):
        return self.longitude


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


def coordArrayCompress(coordArray, samplingInteval):
    #compress coord points in coordArray
    dataArray = []
    i = 0
    while i < len(coordArray):
        flo = floor(coordArray[i].time / samplingInteval)
        flo = int(flo)
        bottom = flo * samplingInteval
        top = (flo + 1) * samplingInteval

        latitudeSum = 0
        longitudeSum = 0
        count = 0
        while i < len(coordArray) and coordArray[i].time in range(bottom, top):
            latitudeSum += coordArray[i].latitude
            longitudeSum += coordArray[i].longitude
            count += 1
            i += 1

        dataArray.append(LocationAndTime(bottom, latitudeSum / count, longitudeSum / count))

    return  dataArray