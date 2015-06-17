# -*- coding = utf-8 -*-
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from senz.views.base import django_view

#from mixpanel import Mixpanel

from SenzPoi.senz.activity.controller import ActivityController

LOG = logging.getLogger(__name__)

@csrf_exempt
@django_view('POST')
def activity_mapping(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''
    body_context = json.loads(request.body)

    controller = ActivityController()
    res = controller.activity_mapping(body_context)

    return res

