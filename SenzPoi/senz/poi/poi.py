# -*- encoding=utf-8 -*-
# __author__ = 'Zhong.zy'

#sys.path.append('../utils')

from SenzPoi.senz.db.avos.avos_manager import *
from SenzPoi.senz.common.utils.util_opt import *
from SenzPoi.senz.common.utils.geo_coding import GeoCoder
from SenzPoi.senz.common.utils.translate import Trans

class PoiGet(object):
    def __init__(self, poi_service='baidu'):
        self.avos = AvosManager()
        self.geo_coder = GeoCoder(poi_service)

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

    def get_nearest_poi(self, lat, lng):
        pois = self.get_poi(lat, lng)
        if not pois:
            return {}

        pois.sort(key=lambda x:x['distance'])

        res_poi = pois[0]
        return dict(name=res_poi['name'], poi_type=Trans.poitype_trans(res_poi['poiType']) )


if __name__ == '__main__':
    a = PoiGet().parse_poi(40.056885091681, 116.30814954222)

    print 'a',a
    for k in a.keys():

        print k,"=", a[k]

