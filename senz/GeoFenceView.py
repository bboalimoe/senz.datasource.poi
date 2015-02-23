__author__ = 'bboalimoe'

import json

from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from mixpanel import Mixpanel



@csrf_exempt
def CreateGeoFence(request):

     """

    /create_geofence/
    description: create the geofence in round and square shape,with unit being mile
    method:                    Post
    data format：              json
    devname(developer):        string
    shape：                     int    “round”：0，“square”：1，
    range:                     number(miles)
    lat                        string
    lng                        string
    FenceGroup                 string

    return：                   {“status”：0(1),"errors":"some errors"(empty)}
    """
