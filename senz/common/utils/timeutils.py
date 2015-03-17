# -*- coding: utf-8 -*-

__author__ = 'wuzhifan'


import time, datetime

ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def iso2timestamp(iso_time): #avos date type {u'__type': u'Date', u'iso': u'2015-05-23T11:15:00.000Z'}
        t = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.000Z")
        return long(time.mktime(t))

def ISOString2Time(s, fmt="%Y-%m-%d %H:%M:%S"):
    '''
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123
    把时间转化为秒
    '''

    d=datetime.datetime.strptime(s,fmt)
    return time.mktime(d.timetuple())

def Time2ISOString(s, fmt="%Y-%m-%d %H:%M:%S"):
    '''
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime(fmt, time.localtime( float(s) ) )


def nowAvosDate():
    #unix epoch time 和 timestamp一致，存入avos后台的utc也是iso和前面是一个转化值。所以呈现出来的string形式，与北京时间不同，差8小时。

    now = time.time()
    utc_time = datetime.datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

    utc_time = utc_time.replace(" ","T")
    return utc_time+".000Z"

def DaysBeforeAvosDate(day):

    before_time = time.time() - day*24*60*60
    utc_time = datetime.datetime.utcfromtimestamp(before_time).strftime('%Y-%m-%d %H:%M:%S')

    utc_time = utc_time.replace(" ","T")
    return utc_time+".000Z"