__author__ = 'bboalimoe'

import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from poi.poiGenerator import PoiGenerator
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel



from senz.activity_spider.runCrawlerTimer import runCrawler, multi_thread_crawl





@csrf_exempt
def TriggerCrawler(request):
    """

    /trigger_crawler/
    description:                  provide api for initiate the Crawler
                                this is to trigger the crawler immediately
                                trigger logic is controlled by outer instance
    method:                    Get

    return：                   {“status”：0(1),"errors":"some errors"(empty)}
    """

    try:
        if request.method == "GET":  #todo refactor with function or decorators
            multi_thread_crawl()
        else:
            return JsonResponse({"status":0},{"errors":"request METHOD illegal"})

    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return JsonResponse({"status":0},{"errors":info})

    return JsonResponse({"status":1})  #indicate the crawl actions have been done


def TriggerCrawlerAtZero(request):
    """
    crawler starts at 24:00:00


    /trigger_crawler_zero/
    description:               crawler starts at 24:00:00
    method:                    Get

    return：                   {“status”：0(1),"errors":"some errors"(empty)}

    """
    try:
        if request.method == "GET":
            runCrawler()

    except:

        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
        return JsonResponse({"status":0})

    return JsonResponse({"status":1}) #indicate the crawl actions have been done
