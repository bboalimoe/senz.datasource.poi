__author__ = 'lsg'

from math import *
from geopy.distance import vincenty

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
    #compress coord points in coordArray for cluster
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
        while i < len(coordArray) and coordArray[i].time >= bottom and coordArray[i].time <= top:
            latitudeSum += coordArray[i].latitude
            longitudeSum += coordArray[i].longitude
            count += 1
            i += 1

        dataArray.append(LocationAndTime(bottom, latitudeSum / count, longitudeSum / count))

    return  dataArray

def is_same_location(new_lng, new_lat, old_lng, old_lat):
    if abs(new_lng - old_lng) < 0.001 and abs(new_lat - old_lat) < 0.001:
        return True
    else:
        return False


def near_place(place, geo_point, near_thres):

    p1 = (place['latitude'], place['longitude'])
    p2 = (geo_point['latitude'], geo_point['longitude'])

    d = vincenty(p1, p2).kilometers

    if(d > near_thres):
        return False
    else:
        return True


