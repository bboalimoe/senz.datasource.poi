# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'


import logging
import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import http

from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
#from mixpanel import Mixpanel


from poi.poiGenerator import PoiGenerator

from senz.poi.controller import PoiController
from senz.exceptions import *

LOG = logging.getLogger(__name__)

"""
发送请求内容：
{
"userId": userID（这个以leancloud里面SenzData里面userInfo表的objectId为准）
"locGPS": [ {
"latitude": latitude,
"longitude": longitude，
"timestamp": timestamp（对应的是这条gps数据数据库中的时间戳，这个时间戳以sdk取出gps数据打上的时间戳为准）
}, ...],
"locBeacon": [ {
"uuid": ibeacon_uuid,
"timestamp": timestamp
}, ...]
}

接受请求结果内容：
{
"GPS": [{

"poiType": POI_TYPE,
"timestamp": timestamp,
"locDescription": DESCRIPTION, （地点位置描述）
"actiTpye": ACTI_TYPE,（活动类型，无则没有这项）
"actiDescription": ACTI_DESCRIPTION,（活动描述，无则没有这项）
"actiStartTime": ACTI_START_TIME（活动开始时间，无则没有这项）
"actiEndTime": ACTI_END_TIME（活动结束时间，无则没有这项）
}, ...]
"iBeacon": [{

"poiType": POI_TYPE,
"timestamp": timestamp,
"locDescription": DESCRIPTION, （地点位置描述）
"actiTpye": ACTI_TYPE,（活动类型，无则没有这项）
"actiDescription": ACTI_DESCRIPTION,（活动描述，无则没有这项）
"actiStartTime": ACTI_START_TIME（活动开始时间，无则没有这项）
"actiEndTime": ACTI_END_TIME（活动结束时间，无则没有这项）
}, ...]
}

"""

def errorInfo():
    import sys
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])  # todo log the exception info
    print info
    return info

def errorResponses(error=None):
    if not error:
        info = errorInfo()
    else:
        info = error

    return JsonResponse({"status": 0}, {"errors": info})


def successResponses(results):

    return JsonResponse({"status": 1, "results": results})



@csrf_exempt
def PoiView(request):

    """

    """
    LOG.info('start get poi')
    try:
        if request.method == 'POST':
            req = json.loads(request.body)  #body is deprecated
        else:
             return errorResponses("Method wrong")
    except:
        return errorResponses()

    userId = req.get("userId")
    GPSlist = req.get("GPS")
    Beaconlist = req.get("iBeacon")

    LOG.info('fetch to poi controller')
    try:
        poiContro = PoiController()
        rtBeaLoc = poiContro.getPoi(Beaconlist, GPSlist, userId)
    except DataCRUDError, e:
        LOG.info('Poi data CRUD error : %s' % e)
        return HttpResponse('Poi data CRUD error : %s' % e, status=DataCRUDError.code)


    print "rtBeaLoc", rtBeaLoc
    return successResponses(rtBeaLoc)

#source /poi/poi.py


@csrf_exempt
def GetBaiduPoiType(request):

    """

    /baidu_poitype/
    description: get the poi type of specific lng&lat in baidu's cloud definition
    method:                    Post
    data format:              json
     lat:                     string
     lng:                      string
    return :{"status":1(0), "results": ["poitype":"","name":""]}


    """

    try:
        if request.method == 'POST':

            req = json.loads(request.body)  #body is deprecated


        else:
             info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
             return JsonResponse({"status":0, "errors":info})
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print info
        return JsonResponse({"status":0,"errors":info})

    lat, lng = req['lat'], req['lng']
    try:
        pg = PoiGet()
        results = pg.parsePoi(lat, lng)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print info

        return JsonResponse({"status":0,"errors":info })


    if not results or "error" in results.keys():
        if not results:
            return JsonResponse({"status":0}, {"errors":'' })
        else:
            return JsonResponse({"status":0}, {"errors":results['error'] })

    else:
        return JsonResponse({"status":1,"results":results})

















