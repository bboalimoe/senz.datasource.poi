# -*- coding = utf-8 -*-
import json
import logging
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from senz.exceptions import *

from django.http import JsonResponse
#from mixpanel import Mixpanel
from senz.activity.UserActivityMapping import UserActivityMapping

LOG = logging.getLogger(__name__)

@csrf_exempt
def UserActivityView(request):
    ''' Parse pois from gps points and if 'userId' in request parmeter
    it will make user activity mapping.

    :param request: django http request
    :return: poi info and user activity mapping results if necessary
    '''
    try:
        if request.method == 'POST':
            body_context = json.loads(request.body)
        else:
            raise BadRequest(resource='activity',
                              msg='unsupported http method ')

        user_id = body_context.get('user_id')
        last_days = body_context.get('last_days')

        controller = UserActivityMapping()
        res = controller.map_user_activity(user_id=user_id, last_days=last_days)


        return JsonResponse({'results': res})

    except AvosCRUDError, e:
        LOG.error('Avos data CRUD error : %s' % e)
        return HttpResponse('Avos data CRUD error : %s' % e, status=AvosCRUDError.code)
    except SenzExcption, e:
        LOG.error('Activity handle error: %s' % e)
        return HttpResponse('Activity handle error: %s' % e, status=SenzExcption.code)
    except Exception, e:
        info, trace = error_info()
        LOG.error(info + ' || ' + str(trace))
        return HttpResponse('System error: %s' % info, status=500)

