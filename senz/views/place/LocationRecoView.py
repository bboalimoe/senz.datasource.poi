#-*- encoding=utf-8 -*-

__author__ = 'bboalimoe'

import json
import logging

import webob
from webob import exc

from django import http

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from mixpanel import Mixpanel

LOG = logging.getLogger(__name__)


from senz.location.LocationRecognition import LocationRecognition



def errorInfo():
    import sys
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])  # todo log the exception info
    print info
    return info

def errorResponses(error=None):
    if not error:
        info = errorInfo()
    else:
        info = error

    return JsonResponse({"status": 0}, {"errors": info})


def successResponses(results):

    return JsonResponse({"status": 1, "results": results})



@csrf_exempt
def GetUserLocationTags(request):
    """

    /usr_loc_tag/
    description:               get the identified place tags for the specified user with POST and userid
                               get all the users' locations tags with GET
    method:                    Post
        userid:                    string
    method:                    Get

    return：                   {“status”：0(1),"errors"(results):"some errors"(results)}
    """

    #todo retrieve data from leancloud or other db
    try:
        locRecg = LocationRecognition()
        if request.method == "POST":  #todo refactor with function or decorators
            req = request.body

            print "body : %s" % req
            bodyData = json.loads(req)
            userId = bodyData["userId"]

            LOG.info("pre place cluster")
            results = locRecg.startCluster(userId)
        elif request.method == "GET":
            results = locRecg.startCluster()
        else:
            return errorResponses("Method wrong")

    except Exception as e:
        LOG.error("get user place tags error : %s" % e)
        return errorResponses()

    return successResponses(results)  #indicate the crawl actions have been done

@csrf_exempt
def AddTraceNearTags(request):
    """

    /add_near_tag/
    description:               add near tag to UserLocationTrace data
    method:                    Post
        userid:                    string
    method:                    Get

    return：                   {“status”：0(1),"errors"(results):"some errors"(results)}
    """
    try:
        req = request.body
        bodyData = json.loads(req)
        userId = bodyData['userId']

        locRecg = LocationRecognition()
        locRecg.addNearTags(userId)

        return successResponses("Add near tag to traces successed!")
    except Exception as e:
        LOG.error("Add user trace near tags error : %s" % e)
        return errorResponses()


def TriggerActions(request):

    """
    ####deprecated####

    trigger the algo to compute all users' identified place tags with GET
                                one user's identified place tags with POST and userid

    logic:
    1.let the algo run until

    /trigger_actions/
    description:               crawler starts at 24:00:00
    method:                    Post
        useid:                     string(if)
    method:                    Get

    return：                   {“status”：0(1),"errors":"some errors"(empty)}

    """
    try:
        if request.method == "POST":
            pass

    except:

        return errorResponses()

    return JsonResponse(successResponses('')) #indicate the crawl actions have been done



