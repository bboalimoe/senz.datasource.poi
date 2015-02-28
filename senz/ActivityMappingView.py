# -*- coding = utf-8 -*-
import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from poi.poiGenerator import PoiGenerator
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel
from senz.activity_user_mapping.UserActivityMapping import UserActivityMapping





@csrf_exempt
def InitiateMapping(request):

    """

        /initial_map/
        description:                initiate mapping actions

        method:                    Get

        return:                   {"status":0(1),"errors":"some errors"(empty)}
    """

    um = UserActivityMapping()
    try:
        um.mapping()

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print info
        return JsonResponse({"status":0,"errors":info})

    return JsonResponse({"status":1})


@csrf_exempt
def GetActivitiesById(request):

        """
            /activity/
            description:                get the mapped 10 activities for the user with the userid

            method:                    POST
             data format:              json
             userId:                  string
             amount:                  int
            return:                   {"status":0(1),"errors":"some errors"(empty)}
        """

        try:

            if request.method == 'POST':
                req = json.loads(request.body)

            else:
                return JsonResponse( {"status":0,"errors":"Method illegal"})
        except:
            import sys
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
            return JsonResponse({"status":0,"errors":info})

        userId, amount = req['userId'], req['amount']
        try:
            um = UserActivityMapping()
            Results = um.mappingActivitiesByUser(userId, int(amount) )
        except:
            import sys
            info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
            return JsonResponse({"status":0, "errors":info})

        return JsonResponse({"status":1, "results":Results["results"][0] })

