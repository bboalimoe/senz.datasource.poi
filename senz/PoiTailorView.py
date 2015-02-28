# -*- encoding=utf-8 -*-

import json

#from django.conf import settings
#settings.configure()   #if we load the django file as one instance, we need first configure the settings

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from poi.poiGenerator import PoiGenerator
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel
import time
#todo change all the users in the poiTailor View to devs


# Create your views here.

mp = Mixpanel('b89d8d933c962ae2e8da4337e29ff829')


def index(request):

    res = ''
    for param, value in request.GET.items():
        res += "%s = %s, " % (param, value)
    print "shuizhaole"
    time.sleep(1000)
    return HttpResponse("senz responses" + res[:-2])





@csrf_exempt
def GetPoiByGeoPointAndDev(request):
    """
    /poi/
    description: get the user-defined the first five nearest poigroup types near the Geopoint
    method:                    Post
    data format：              json
    devname(developer):       string
    lat                        string
    lng                        string
    return :{"status":0(1), "results": [poitype1,type2]}
    """


    try:
        if request.method == 'POST':
            print 'request.body  ', request.body

            print "type of body ", type(request.body)
            req = json.loads(request.body)  #body is deprecated

        else:

            return JsonResponse({"status":0})
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        print "info    ", info
        print 'fuck'
        return JsonResponse({"status":0})



    poi = PoiGenerator()
    devname, lat, lng = req['devname'], req['lat'], req['lng']
    pois = poi.getPoiGroupByGps(devname, int(lat), int(lng))


    return JsonResponse(dict(status=1, results=pois))   # response in JSON style

@csrf_exempt
def GetDevPoiGroups(request):
    """

    /poi_groups/
    description: get all the poi groups the specific user defined
    method:                    Post
    data format：              json
    devname(developer):       string

    return :{"status":0(1), "results": [poitype1,type2,...]}


    """
    try:
        if request.method == 'POST':

            req = json.loads(request.body)  #body is deprecated

        else:

            return JsonResponse({"status":0})
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info

        return JsonResponse({"status":0})

        devname = req['devname']
    try:
        poi = PoiGenerator()
        results = poi.getPoiGroups(devname)

    except:
        return JsonResponse({"status":0})

    if not results or "error" in results.keys():
        if not results:
            return JsonResponse({"status":0}, {"errors":'' })
        else:
            return JsonResponse({"status":0}, {"errors":results['error'] })

    else:
        return JsonResponse({"status":1})


@csrf_exempt
def PoiGroup(request):

    """

     /poi_group/
     description: create /delete the poi group type
     method:                    Post / Delete
     data format：              json
     devname:                 string
     poiGroupType:             string
     return：                   {“status”：0(1),"errors":"some errors"(empty)}



"""

    try:
        if request.method in ['POST',"PUT","DELETE"]:
            req = json.loads(request.body)
        else:
            return JsonResponse({"status":0})

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return JsonResponse({"status":0})

    devname, poiGroupType = req['devname'], req['poiGroupType']
    poi = PoiGenerator()
    try:
        if request.method is "POST":
            results = poi.addPoiGroupByName(poiGroupType, devname)
        if request.method is "DELETE":
            results = poi.deletePoiGroupByName(poiGroupType, devname)

    except :
        #todo log the error
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return JsonResponse({"status":0},{"errors":info})  # 0 failure; 1 success
    if results:
        return JsonResponse({"status":1}) #todo response with results in json
    else:
        return JsonResponse({"status":0, "errors":results["error"]})



@csrf_exempt
def PoiGroupMember(request):   #todo : aggregate post, delete, put
                                 # todo: update return params logic are diffrent from other 2.

    """

      /poi_group_member/
     description: create/update/delete the poi group member
     method:                    Post / PUT / DELETE
     data format：              json
     devname:                 string
     poiGroupType:             string
     lat:                      string
     lng                        string
     return：                   {“status”：0(1),"errors":"some errors"(empty)}


"""


    try:
        if request.method == ['POST',"PUT","DELETE"]:
            req = json.loads(request.body)
        else:
            return JsonResponse({"status":0})

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return HttpResponse(None)
    
    devname, lat, lng, poiGroupType = req['devname'], req['lat'], req['lng'], req['poiGroupType']
    poi = PoiGenerator()
    try:
        if request.method == "POST":
            results = poi.addPoiGroupMemberByName(poiGroupType,devname,lat,lng)
        elif request.method == "DELETE":
            results = poi.deletePoiGroupMemberByName(poiGroupType,devname,lat,lng)
        elif request.method == "PUT":
            results = poi.updatePoiGroupMemberByName(poiGroupType,devname,lat,lng)
        else:
            return HttpResponse(None)


    except:
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return JsonResponse({"status":0},{"errors":info})  # 0 failure; 1 success
    if not results or "error" in results.keys():

        return JsonResponse({"status":0},{"errors":results["error"]})
    else:
        return JsonResponse({"status":1}) #todo response with results in json






