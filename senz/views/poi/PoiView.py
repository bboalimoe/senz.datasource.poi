# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'


import logging
import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from mixpanel import Mixpanel

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

#has not beacon process now
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

#has not beacon process now
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

@csrf_exempt
def PoiView(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''
    try:
        if request.method == 'POST':
            req = json.loads(request.body)
        else:
            raise BadRequest(resource='poi',
                              msg='unsupported http method ')

        userId = req.get('userId')
        gpsList = req.get('GPS')

        poiContro = PoiController()
        res = poiContro.getPoi(gpsList, userId)

        return JsonResponse({'results': res})

    except DataCRUDError, e:
        LOG.error('Poi data CRUD error : %s' % e)
        return HttpResponse('Poi data CRUD error : %s' % e, status=DataCRUDError.code)
    except SenzExcption, e:
        LOG.error('Poi parse handle error: %s' % e)
        return HttpResponse('Poi parse handle error: %s' % e, status=SenzExcption.code)
    except Exception, e:
        info = errorInfo()
        LOG.error(info)
        return HttpResponse('System error: %s' % info, status=500)


