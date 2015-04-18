#-*- encoding=utf-8 -*-

__author__ = 'wuzhifan'

import json
import logging

from senz.place.LocationRecognition import LocationRecognition
from senz.views.base import django_view

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from mixpanel import Mixpanel

LOG = logging.getLogger(__name__)

@csrf_exempt
@django_view('POST')
def GetUserLocationTags(request):
    """
    description:             places recognition of user identified by 'user_id'
    """
    body_context = json.loads(request.body)

    user_id = body_context.get('user_id')
    sampling_interval = body_context.get('sampling_interval')
    time_threshold = body_context.get('time_threshold')

    place_recg = LocationRecognition()

    LOG.debug('Pre places recognition')
    print sampling_interval
    print time_threshold
    results = place_recg.startCluster(user_id, sampling_interval, time_threshold)
    return results






