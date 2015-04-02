# -*- encoding=utf-8 -*-
__author__ = 'wuzhifan'


import logging
import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from mixpanel import Mixpanel

from senz.poi.controller import PoiController
from senz.exceptions import *

LOG = logging.getLogger(__name__)

@csrf_exempt
def PoiView(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''
    try:
        if request.method == 'POST':
            requestData = json.loads(request.body)
        else:
            raise BadRequest(resource='poi',
                              msg='unsupported http method ')

        poiController = PoiController()
        res = poiController.parse(requestData)

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


