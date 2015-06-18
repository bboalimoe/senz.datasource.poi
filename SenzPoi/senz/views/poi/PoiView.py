# -*- encoding=utf-8 -*-
__author__ = 'wuzhifan'

import logging
import json

from django.views.decorators.csrf import csrf_exempt




#from mixpanel import Mixpanel

from senz.poi.controller import PoiController
from senz.views.base import django_view

LOG = logging.getLogger(__name__)

@csrf_exempt
@django_view('POST')
def parse_poi(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''

    LOG.debug('*****************  test log entries ********************')

    print "pre poi parse"

    body_context = json.loads(request.body)

    controller = PoiController()
    res = controller.parse(body_context)

    return res


