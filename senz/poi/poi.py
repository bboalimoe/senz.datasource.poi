# -*- encoding=utf-8 -*-
# __author__ = 'Zhong.zy'

import sys
#sys.path.append('../utils')

import json
from senz.utils.avos_manager import *
from senz.utils.util_opt import *
from senz.utils.geo_coding import GeoCoder
from senz.utils.translate import Trans

class PoiGet(object):
    def __init__(self):
        self.avos = AvosManager()
        self.geo = None

    def getPoi(self, lat, lng):
        self.geo = GeoCoder()
        return self.geo.getPOI(lat, lng)

    def get(self, device_id, developer_id, location, beacon):
        user = dict(__type='Pointer', className='_User', objectId=developer_id)
        lat, lng = float(location['latitude']), float(location['longitude'])
        if beacon:
            lat, lng = self.getLocation(beacon)
        gps = dict(__type='GeoPoint', latitude=lat, longitude=lng)
        dataDict = {"device_id": device_id, "developer": user, "accuracy": location['accuracy'],
                    "time": location['time'], "gps": gps, "speed": location['speed']}
        self.avos.saveData('Location', dataDict)
        poi = self.getPoi(lat, lng)
        return dict(at=poi)

    def parsePoi(self, lat, lng):


        poi = self.getPoi(lat, lng)

        trans = Trans()
        return dict(name=poi['name'], poiType=trans.poitype_trans(poi['poiType']) )


if __name__ == '__main__':
    a = PoiGet().parsePoi(40.056885091681, 116.30814954222)

    print 'a',a
    for k in a.keys():

        print k,"=", a[k]

