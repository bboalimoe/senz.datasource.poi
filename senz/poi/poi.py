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

        "return {'poiType': 'estate', 'name': u'\u767e\u5ea6\u5927\u53a6'} "
        poi = self.getPoi(lat, lng)

        trans = Trans()
        # poi {u'distance': u'0', u'direction': u'\u5185', u'poiType': u'\u623f\u5730\u4ea7', u'tel': u'', u'addr': u'\u5317\u4eac\u5e02\u6d77\u6dc0\u533a\u4e0a\u5730\u5341\u885710\u53f7', u'zip': u'', u'point': {u'y': 40.056968205361, u'x': 116.30768368099}, u'uid': u'435d7aea036e54355abbbcc8', u'cp': u'NavInfo', u'name': u'\u767e\u5ea6\u5927\u53a6'}

        print "poi",poi
        if not poi:
            return dict(name="", poiType="" )

        return dict(name=poi['name'], poiType=trans.poitype_trans(poi['poiType']) )


if __name__ == '__main__':
    a = PoiGet().parsePoi(40.056885091681, 116.30814954222)

    print 'a',a
    for k in a.keys():

        print k,"=", a[k]

