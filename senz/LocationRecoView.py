__author__ = 'bboalimoe'

import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from mixpanel import Mixpanel


from senz.location_recognition.location import startCluster


def errorInfo():
    import sys
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])  # todo log the exception info
    return info

def errorResponses():
    info = errorInfo()
    return JsonResponse({"status": 0}, {"errors": info})


def successResponses(results):
    return {"status": 1, "results": results}


@csrf_exempt
def GetUserLocationTags(request):

    """

    /usr_loc_tag/
    description:               get the identified location tags for the specified user with POST and userid
                               get all the users' locations tags with GET
    method:                    Post
        userid:                    string
    method:                    Get

    return：                   {“status”：0(1),"errors"(results):"some errors"(results)}
    """

    #todo retrieve data from leancloud or other db
    try:
        if request.method is "POST":  #todo refactor with function or decorators
           req = request.body
        elif request.method == "GET":
            results = startCluster()
            return JsonResponse(successResponses(results))  #indicate the crawl actions have been done
        else:
            return JsonResponse({"status":0},{"errors":"request METHOD illegal"})

    except:
        return errorResponses()

    userid = req["userid"]
    try:
        results = startCluster(userid)
    except:
        return errorResponses()

    return JsonResponse(successResponses(results))  #indicate the crawl actions have been done



def TriggerActions(request):

    """
    ####deprecated####

    trigger the algo to compute all users' identified location tags with GET
                                one user's identified location tags with POST and userid

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
