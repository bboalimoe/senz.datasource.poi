#!/usr/bin/env python
# encoding: utf-8

# use (id,key) or X-AVOSCloud-Request-Sign to auth
# https://cn.avoscloud.com/docs/rest_api.html

#avos_app_id = 'vigxpgtjk8w6ruxcfaw4kju3ssyttgcqz38y6y6uablqivjd'
#avos_app_key = 'dxbawm2hh0338hb37wap59gticgr92dpajd80tzekrgv1ptw'
#avos_app_master_key = 'u0nu3suqria905en9gbq7isetlf5exoqmndv4fxcfck26kdr'

groups = {
    'base' : {
        'avos_app_id' : 'vigxpgtjk8w6ruxcfaw4kju3ssyttgcqz38y6y6uablqivjd',
        'avos_app_key': 'dxbawm2hh0338hb37wap59gticgr92dpajd80tzekrgv1ptw',
        'avos_app_master_key' : 'u0nu3suqria905en9gbq7isetlf5exoqmndv4fxcfck26kdr',
        'avos_app_classes_list' : []
    },
    'place' : {
        'avos_app_id' : 'h1ii4cs01bqlc94at5l3rzngwmiembappirqdo22z2p1e610',
        'avos_app_key': 'qmdhudhx52mnr68euhiwavsloekaox3xp120lflvo5f91do5',
        'avos_app_master_key' : 'n2tskry5otv71ldaj0sylevhfe2h2uww0l3d0bk71mqffiz3',
        'avos_app_classes_list' : ['LocationRecognition',]
    },
    'life_logger' : {
        'avos_app_id' : 'gaqzfcjhsbtoug7a2pnc21r3q7noots1u1we4002pyohbctv',
        'avos_app_key': 'df2et5hn1wervr4j2ajas0bvgvwk90zezlsl1oq0zzmckbsy',
        'avos_app_master_key' : 'bz4xik4o8xo8s60zl0uxhyf8nhx976ddmkjdcv6xtz2lms3l',
        'avos_app_classes_list' : []
    },
    'data_sample' : {
        'avos_app_id' : 'mlg6g76on2b8xqzu2e2ghc2vkm4f0214smqgwzvg195qajbj',
        'avos_app_key': '7pu1411dmmuvrv51caudehxa1c7sdjcle07nh4knja6sm59m',
        'avos_app_master_key' : 'gypoj3dzxgc2mqnm77ehwb6y17k4ks28ylvlj5lf2kx8nbei',
        'avos_app_classes_list' : ['UserLocation',]
    },
}

#function names
PARSE_POI = 'parse_poi'
ACTIVITY_MAPPING = 'activity_mapping'
BEACON = 'beacon'
PLACE_RECOGNITION = 'place_recognition'
INTERNAL_PLACE_RECOGNITION = 'internal_place_recognition'
GEO_FENCE = 'geo_fence'
POI_GROUP = 'poi_group'


#store types
RAW = 'raw'
RESULTS = 'results'

poi_group_task = {
    'type' : 'collection',
    'manager' : 'senz.poi.manager.PoiGroupManager',
    'group_add' : {
        'args' : ['name'],
        'type' : 'task'
    }
}

tasks = {

    PARSE_POI : {
        'manager' : 'senz.poi.manager.PoiManager',
        'args' : ['gps',],
        'store' : [],
        'type' : 'task'
    },
    ACTIVITY_MAPPING : {
        'manager' : 'senz.activity.manager.ActivityManager',
        'args' : ['gps', 'user_id'],
        'store' : [],
        'type' : 'task'
    },
    PLACE_RECOGNITION : {
        'manager' : 'senz.place.manager.PlaceManager',
        'method' : 'place_recognition',
        'store' : [RAW, RESULTS],
        'type' : 'task'
    },
    INTERNAL_PLACE_RECOGNITION : {
        'manager' : 'senz.place.manager.PlaceManager',
        'method' : 'internal_place_recognition',
        'store' : [RESULTS],
        'type' : 'task'
    },

    BEACON : {
        'type' : None
    },
    GEO_FENCE : {
        'type' : None
    },
    POI_GROUP : poi_group_task,
}

controllers = {
    'PoiController' : {
        #'class' : PoiController,
        'jobs' : {
            'parse' : [ACTIVITY_MAPPING, PARSE_POI]
        }
    },
    'PlaceController' : {
        #'class' : PoiController,
        'jobs' : {
            'place_recognition' : [PLACE_RECOGNITION,],
            'internal_place_recognition' : [INTERNAL_PLACE_RECOGNITION,],
        }
    }
}