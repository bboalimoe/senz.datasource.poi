poi module

##APIs

POST  /senz/pois/    解析位置数据poi信息

Request parameters(in json):

locations : (list) 位置数据
user_id : (string) 位置数据相关的user (optional)
poi_type : (string) 需要获取的poi类别 (optional)

request body(json):
{
    'poi_type' : 'hotel',
    'user_id' : '12345678',
    'locations' : [{'timestamp': 1427642632501L, 'location': {'latitude': 39.9874398746627, '__type': u'GeoPoint', 'longitude': 116.438323511219053}}}, ... ...],
}

Response(Json form):
{"results":
    {"parse_poi":
        [
           {'timestamp': 1427642632501L,
            'location': {'latitude': 39.987433, '__type': u'GeoPoint', 'longitude': 116.438513},
            'pois' : [
                        {u'distance': u'0', u'direction': u'内', u'poiType': u'房地产', u'tel': u'',
                         u'addr': u'芍药居北里芍药居', u'zip': u'',
                         u'point': {u'y': 39.988191941116, u'x': 116.43765052217},
                         u'uid': u'6fddd7fdfcc7ea7f3417dc8c', u'cp': u'NavInfo', u'name': u'芍药居5号院'},
                         ... ...
                     ]
            },
            ... ...
        ]
    },
}
