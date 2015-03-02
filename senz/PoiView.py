# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'


from senz.poi.poi import PoiGet
from senz.activity_user_mapping.UserActivityMapping import UserActivityMapping
from senz.poi.beacon import Beacon
import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from poi.poiGenerator import PoiGenerator
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel


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
    return info

def errorResponses(error=None):
    if not error:
        info = errorInfo()
    else:
        info = error

    return JsonResponse({"status": 0}, {"errors": info})


def successResponses(results):
    return {"status": 1, "results": results}



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
"""


@csrf_exempt
def GetPoi(request):

    """

    """
    try:
        if request.method == 'POST':
            req = json.loads(request.body)  #body is deprecated
        else:
             return errorResponses("Method wrong")
    except:
        return errorResponses()

    userId = req["userId"]
    GPSlist = req["locGPS"]
    GPSlen = len(GPSlist)
    Beaconlist = req["locBeacon"]
    Beaconlen = len(Beaconlist)



    #todo 1.每来一次请求就把数据存入后端 2.beacon和gps数据存完后，调用匹配算法算制定userid匹配出的活动
    try:

        GPSrtList = [{} for i in range(GPSlen)]

        BeaconrtList = [{} for i in range(Beaconlen)]

        usermapping = UserActivityMapping()
        beacon = Beacon()
        pg = PoiGet()
        usermapping.dump2db(GPSlist,userId)
        beacon.dump2db(Beaconlist,userId)

        #todo
        for gps,i in GPSlist,range(GPSlen):



            #gps poitype

            results = pg.parsePoi(gps["latitude"], gps["longitude"])
            poiType, poiName = results['poiType'], results['name']
            GPSrtList[i].setdefault("poiType",poiType)
            GPSrtList[i].setdefault("locDescription",poiName)  #poiname => locDescription
            GPSrtList[i].setdefault("timestamp",gps['timestamp'])




    except:

        return errorResponses()


    if not results or "error" in results.keys():
        if not results:

            return errorResponses('')

        else:
            return errorResponses(results['error'])


    else:
        return successResponses(results)



















