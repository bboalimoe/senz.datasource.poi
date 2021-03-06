#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from senz.db.avos.avos_manager import *

sources = {
    #todo: make poi services metadate !!!!!!
    'baidu' : {
        'urls' : {
            'get_poi' : "http://api.map.baidu.com/geocoder/v2/?coordtype=bd09ll&location=%s,%s&output=json&ak=fPnXQ2dVgLevy7GwIomnhEMg&pois=1",
        },
        'poi_type_name' : 'poiType',
        'location_name_info' : {
            'name' : 'point',
            'latitude' : 'y',
            'longitude' : 'x'
        }
    },
    'tencent' : {
        'urls' : {
            'get_poi' : "http://apis.map.qq.com/ws/geocoder/v1/?location=%s,%s&key=PIZBZ-GUQWJ-FQ4FT-K72GW-LPCAZ-HEB24&get_poi=1",
        },
        'poi_type_name' : 'category',
        'location_name_info' : {
            'name' : 'location',
            'latitude' : 'lat',
            'longitude' : 'lng'
        }
    }
}

DEFAULT_BAIDU_POI_MAPPING = {
u"休闲娱乐":"entertainment",
u"地产小区":"estate",
u"政府机构":"infrastructure",
u"餐饮":"dining",
u"教育":"education",
u"交通设施":"infrastructure",
u"金融":"finance",
u"行政地标":"scenic_spot",
u"旅游景点":"scenic_spot",
u"其他":"unknown",
u"房地产":"estate",
u"other":"unknown",
u"美食":"dining",
u"生活服务":"life_service",
u"公司企业":"estate",
u"购物":"shopping",
u"教育培训":"education",
u"汽车服务":"auto_related",
u"医疗":"healthcare",
u"酒店":"hotel"
}


class GeoCoder(object):
    def __init__(self, poi_service='baidu', coord_type='baidu'):
        self.source = sources.get(poi_service, None)
        self.poi_service = poi_service
        if self.source == None:
            raise SenzExcption(msg='unkown poi service type.')

        self.coord_type = coord_type
        self.avos_manager = AvosManager()
        self.tecent_poi_types = self.avos_manager.getAllData('poi_types')

    def geoCoding(self,region):
        url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=fPnXQ2dVgLevy7GwIomnhEMg&callback=showLocation" % region
        result_info = get_source(url)
        try:
            lng_1 = float(re.findall(r'(?<=lng\":)[^,]+(?=,)', result_info)[0])
            lat_1 = float(re.findall(r'(?<=lat\":)[^}]+(?=})', result_info)[0])
        except:
            return 0.0,0.0
        #type
        poiType = json.loads(result_info[27:-1])['result']['level']

        #convert
        #lng,lat = self.convert(lng_1,lat_1)
        #save to avos
        #dataDict = {'name':region,'type':poiType,'lattitude':lat,'longitude':lng}
        #avosManager = AvosManager()
        #avosManager.updateDataByName('poiClass',region,dataDict)
        return lng_1,lat_1

    def convert(self,lng_1,lat_1):
        #convert
        convert_url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&ak=fPnXQ2dVgLevy7GwIomnhEMg&from=1&to=5&output=json&callback=BMap.Convertor.cbk_7594' % (lng_1,lat_1)
        convert_info = get_source(convert_url)
        try:
            lng_2 = float(re.findall(r'(?<=x\":)[^,]+(?=,)', convert_info)[0])
            lat_2 = float(re.findall(r'(?<=y\":)[^}]+(?=})', convert_info)[0])
        except:
            return lng_1,lat_1
        lng = 2*lng_1 - lng_2
        lat = 2*lat_1 - lat_2
        return lng,lat

    def get_poi(self,lat,lng):
        #url =  % (lat,lng)

        url = self.source['urls'].get('get_poi', None)
        if not url:
            raise SenzExcption(msg='Can not find poi parse service url.')

        if self.poi_service == 'tencent' and self.coord_type == 'baidu':
            url += '&coord_type=3'

        #print "i am changed !!!!!!!!"
        url =  url % (lat,lng)
        result_info = get_source(url)

        res_dict = json.loads(result_info)
        #LOG.info('in geo coding result %s' % result_info)
        if res_dict['status'] != 0:
            return None #todo return the error info that baidu returns
        #print "details   ", a
        #print(json.loads(result_info)['result'])
        pois = res_dict['result']['pois']
        if not pois:
            return {}
        #poi = pois[1]['name']
        #return poi.encode('utf-8')
        #LOG.info("in geo coding return poi %s" % pois[0])


        def mapping_poi_type(type):
            #print "poi types len %d" % len(self.poi_types)
            if self.poi_service == 'tencent':
                poi_types = self.tecent_poi_types
            else:
                poi_types = DEFAULT_BAIDU_POI_MAPPING

            for t in poi_types:
                if self.poi_service == 'tencent' and t['origin_type'].find(type) >= 0:
                    return t
                elif t == type:
                    return dict(mapping_type=t, type=type, source=self.poi_service)

            return dict(mapping_type='unkown', type=type, source=self.poi_service)

        def transfer_location_name(poi):
            location_name_info = self.source['location_name_info']
            latitude = poi[location_name_info['name']][location_name_info['latitude']]
            longitude = poi[location_name_info['name']][location_name_info['longitude']]

            del poi[location_name_info['name']]

            poi['location'] = {'latitude' : latitude, 'longitude' : longitude}



        for p in pois:

            senz_poi_type = mapping_poi_type(p[self.source['poi_type_name']])
            del p[self.source['poi_type_name']]
            p['type'] = senz_poi_type

            print p

            transfer_location_name(p)

        return pois

    def getPOIByName(self,name):
        url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=fPnXQ2dVgLevy7GwIomnhEMg&pois=1" % name
        result_info = get_source(url)
        #print(json.loads(result_info)['result'])



if __name__ == "__main__":
    geo = GeoCoder()
    #region = "​中国票务在线上海站"
    #lng,lat=geo.geoCoding(region)
    #print lng,lat
    lng = 116.43832351121905
    lat = 39.9874398746627
    res = geo.get_poi(lat, lng)
    #print str(res)
    print res['direction']
    print res['poiType']
    print res['addr']
    print res['name']
    #print geo.getPOI(39.936691964083,116.45062456899)
    #print geo.getPOIByName("北京香河");
