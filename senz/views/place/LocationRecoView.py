#-*- encoding=utf-8 -*-

__author__ = 'wuzhifan'

import json
import logging

#from senz.place.controller import PlaceController

from senz.place.LocationRecognition import LocationRecognition

from senz.views.base import django_view

from django.views.decorators.csrf import csrf_exempt
#from mixpanel import Mixpanel

LOG = logging.getLogger(__name__)

@csrf_exempt
@django_view('POST')
def get_user_places(request):
    """
    description:             places recognition of user identified by 'user_id'
    """
    body_context = json.loads(request.body)

    #controller = PlaceController()

    LOG.debug('Pre places recognition')
    #results = controller.place_recognition(body_context)


    #return results


@csrf_exempt
@django_view('POST')
def internal_get_user_places(request):
    """
    description:             senz internal places recognition of user identified by 'user_id'
    """
    body_context = json.loads(request.body)
    '''
    controller = PlaceController()

    LOG.debug('Pre places recognition')
    results = controller.internal_place_recognition(body_context)
    '''

    manager = LocationRecognition()
    results = manager.startCluster('no_user', body_context.get('user_trace'))
    return results




