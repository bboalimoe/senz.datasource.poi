#!/usr/bin/env python
# encoding: utf-8

# use (id,key) or X-AVOSCloud-Request-Sign to auth
# https://cn.avoscloud.com/docs/rest_api.html

#avos_app_id = 'vigxpgtjk8w6ruxcfaw4kju3ssyttgcqz38y6y6uablqivjd'
#avos_app_key = 'dxbawm2hh0338hb37wap59gticgr92dpajd80tzekrgv1ptw'
#avos_app_master_key = 'u0nu3suqria905en9gbq7isetlf5exoqmndv4fxcfck26kdr'

#todo: dispatch modules configurations in system init

groups = {
    'origin' : {
        'avos_id' : 'vigxpgtjk8w6ruxcfaw4kju3ssyttgcqz38y6y6uablqivjd',
        'avos_key': 'dxbawm2hh0338hb37wap59gticgr92dpajd80tzekrgv1ptw',
        'avos_master_key' : 'u0nu3suqria905en9gbq7isetlf5exoqmndv4fxcfck26kdr',
        'avos_classes_list' : []
    },
    'location' : {
        'avos_id' : 'h1ii4cs01bqlc94at5l3rzngwmiembappirqdo22z2p1e610',
        'avos_key': 'qmdhudhx52mnr68euhiwavsloekaox3xp120lflvo5f91do5',
        'avos_master_key' : 'n2tskry5otv71ldaj0sylevhfe2h2uww0l3d0bk71mqffiz3',
        'avos_classes_list' : ['LocationRecognition',]
    }
}