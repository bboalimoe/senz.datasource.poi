#!/usr/bin/env python
# encoding: utf-8

# use (id,key) or X-AVOSCloud-Request-Sign to auth
# https://cn.avoscloud.com/docs/rest_api.html

#avos_app_id = 'vigxpgtjk8w6ruxcfaw4kju3ssyttgcqz38y6y6uablqivjd'
#avos_app_key = 'dxbawm2hh0338hb37wap59gticgr92dpajd80tzekrgv1ptw'
#avos_app_master_key = 'u0nu3suqria905en9gbq7isetlf5exoqmndv4fxcfck26kdr'

from senz.poi.manager import PoiManager, PoiGroupManager
from senz.activity.manager import ActivityManager
from senz.poi.controller import PoiController

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
    }
}


poi_group_func = {
    'type' : 'collection',
    'manager' : PoiGroupManager(),
    'group_add' : {
        'args' : ['name'],
        'type' : 'func'
    }
}

functions = {
    'parse_poi' : {
        'manager' : PoiManager(),
        'args' : ['gps',],
        'store' : False,
        'type' : 'func'
    },
    'activity_mapping' : {
        'manager' : ActivityManager(),
        'args' : ['gps', 'user_id'],
        'store' : False,
        'type' : 'func'
    },
    'place_recognition': {

    },
    'beacon' : {

    },
    'geo_fence' : {

    },
    'poi_group' : poi_group_func,
}

controllers = {
    'poi' : {
        'class' : PoiController,
        'methods' : {
            'parse' : ['parse_poi', 'activity_mapping']
        }
    }
}