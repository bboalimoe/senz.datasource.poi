__author__ = 'bboalimoe'

from senz.poi.poi import PoiGet

import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from poi.poiGenerator import PoiGenerator
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel

#source /poi/poi.py


@csrf_exempt
def GetBaiduPoiType(request):

    """

    /baidu_poitype/
    description: get the poi type of specific lng&lat in baidu's cloud definition
    method:                    Post
    data format:              json
     lat:                     string
     lng:                      string
    return :{"status":1(0), "results": ["poitype":"","name":""]}


    """

    try:
        if request.method == 'POST':

            req = json.loads(request.body)  #body is deprecated


        else:
             info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
             return JsonResponse({"status":0, "errors":info})
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print info
        return JsonResponse({"status":0,"errors":info})

    lat, lng = req['lat'], req['lng']
    try:
        pg = PoiGet()
        results = pg.parsePoi(lat, lng)

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print info

        return JsonResponse({"status":0,"errors":info })


    if not results or "error" in results.keys():
        if not results:
            return JsonResponse({"status":0}, {"errors":'' })
        else:
            return JsonResponse({"status":0}, {"errors":results['error'] })

    else:
        return JsonResponse({"status":1,"results":results})


