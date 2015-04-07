# -*- encoding=utf-8 -*-
# __author__ = 'Zhong.zy'

#sys.path.append('../utils')

from senz.common.avos.avos_manager import *
from senz.common.utils.util_opt import *
from senz.common.utils.geo_coding import GeoCoder
from senz.common.utils.translate import Trans

class PoiGet(object):
    def __init__(self):
        self.avos = AvosManager()
        self.geo_coder = GeoCoder()

    def get_poi(self, lat, lng):
        return self.geo_coder.get_poi(lat, lng)

    def get(self, device_id, developer_id, location, beacon):
        user = dict(__type='Pointer', className='_User', objectId=developer_id)
        lat, lng = float(location['latitude']), float(location['longitude'])
        if beacon:
            lat, lng = self.getLocation(beacon)
        gps = dict(__type='GeoPoint', latitude=lat, longitude=lng)
        dataDict = {"device_id": device_id, "developer": user, "accuracy": location['accuracy'],
                    "time": location['time'], "gps": gps, "speed": location['speed']}
        self.avos.saveData('Location', dataDict)
        poi = self.get_poi(lat, lng)
        return dict(at=poi)

    def parse_poi(self, lat, lng):
        poi = self.get_poi(lat, lng)
        if not poi:
            return {}
        return dict(name=poi['name'], poi_type=Trans.poitype_trans(poi['poiType']) )


if __name__ == '__main__':
    a = PoiGet().parse_poi(40.056885091681, 116.30814954222)

    print 'a',a
    for k in a.keys():

        print k,"=", a[k]

