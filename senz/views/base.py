# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import logging
import json
import traceback
import sys

from django.http.response import HttpResponse, JsonResponse

from senz.exceptions import *

LOG = logging.getLogger(__name__)


def django_view(http_method):
    def wrapper(func):
        def view_base(request, **kwargs):
            ''' views common process

            :param request: django request
            :param kwargs: other django view args
            :return: view result
            '''
            try:
                if request.method == http_method:
                    body_context = json.loads(request.body)
                else:
                    raise BadRequest(msg='unsupported http method ')

                LOG.debug('Got request to %s.' % func.func_name)
                results = func(request, **kwargs)

                if not isinstance(results, (dict, str)):
                    results = str(results)

                return JsonResponse({'results':results})

            except SenzExcption, e:
                LOG.error('Request %s error: %s' % (func.func_name, e))
                return HttpResponse('Request %s encounter internal error: %s' % (func.func_name, e),
                                                                    content_type='text/plain',
                                                                    status=SenzExcption.code)
            except Exception as e:
                LOG.error(traceback.print_exception(*(sys.exc_info())))
                info, trace= error_info()
                #LOG.error(info + '||' + trace.print_exc())
                return HttpResponse('System error: %s' % info, content_type='text/plain',status=500)

        return view_base
    return wrapper