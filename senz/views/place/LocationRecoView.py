#-*- encoding=utf-8 -*-

__author__ = 'bboalimoe'

import json
import logging

from senz.place.LocationRecognition import LocationRecognition

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from mixpanel import Mixpanel

from senz.exceptions import *

LOG = logging.getLogger(__name__)



@csrf_exempt
def GetUserLocationTags(request, user_id):
    """
    description:             places recognition of user identified by 'user_id'
    """
    try:
        place_recg = LocationRecognition()
        '''
        if request.method == 'GET':
            user_id = request.GET['user_id']
        else:
            raise BadRequest(resource='poi',
                              msg='unsupported http method ')
                              '''

        LOG.info('Pre places recognition')
        results = place_recg.startCluster(user_id)
        return JsonResponse({'results':results})

    except SenzExcption, e:
        LOG.error('Poi parse handle error: %s' % e)
        return HttpResponse('Poi parse handle error: %s' % e, status=SenzExcption.code)

    except Exception as e:
        info = error_info()
        LOG.error(info)
        return HttpResponse('System error: %s' % info, status=500)


@csrf_exempt
def AddTraceNearTags(request, user_id):
    """
    description:               add near tag to UserLocationTrace data of user identified by 'user_id'
    """
    try:
        place_recg = LocationRecognition()
        '''
        if request.method == 'GET':
            user_id = request.GET['user_id']
        else:
            raise BadRequest(resource='poi',
                              msg='unsupported http method ')
                              '''

        place_recg.addNearTags(user_id)

        return HttpResponse("Add near tag to traces succeed")

    except SenzExcption, e:
        LOG.error('Poi parse handle error: %s' % e)
        return HttpResponse('Poi parse handle error: %s' % e, status=SenzExcption.code)

    except Exception as e:
        info = error_info()
        LOG.error(info)
        return HttpResponse('System error: %s' % info, status=500)





