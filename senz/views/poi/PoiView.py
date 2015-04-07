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

PARSE_METHOD_NAME = 'parse'

@csrf_exempt
def PoiView(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''
    try:
        if request.method == 'POST':
            body_context = json.loads(request.body)
        else:
            raise BadRequest(resource='poi',
                              msg='unsupported http method ')

        controller = PoiController()
        res = controller.parse(body_context)

        return JsonResponse({'results': res})

    except DataCRUDError, e:
        LOG.error('Poi data CRUD error : %s' % e)
        return HttpResponse('Poi data CRUD error : %s' % e, status=DataCRUDError.code)
    except SenzExcption, e:
        LOG.error('Poi parse handle error: %s' % e)
        return HttpResponse('Poi parse handle error: %s' % e, status=SenzExcption.code)
    except Exception, e:
        info = error_info()
        LOG.error(info)
        return HttpResponse('System error: %s' % info, status=500)


