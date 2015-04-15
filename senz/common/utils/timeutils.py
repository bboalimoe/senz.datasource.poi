# -*- coding: utf-8 -*-

__author__ = 'wuzhifan'


import time, datetime


ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def iso2timestamp(iso_time): #avos date type {u'__type': u'Date', u'iso': u'2015-05-23T11:15:00.000Z'}
        t = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.%fZ")
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
    utc_time = datetime.datetime.utcfromtimestamp(now).strftime(ISO_TIME_FORMAT)
    return utc_time

def DaysBeforeAvosDate(day):

    before_time = time.time() - day*24*60*60
    utc_time = datetime.datetime.utcfromtimestamp(before_time).strftime(ISO_TIME_FORMAT)
    return utc_time

def locol_utc_offset():
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    return local_time - utc_time

LOCAL_UTC_OFFSET = locol_utc_offset()

def utc2local(utc_st):
    '''convert utc datetime to local datetime

    :param utc_st: datetime.datetime type
    :return:
    '''
    local_st = utc_st + LOCAL_UTC_OFFSET
    return local_st

def local2utc(local_st):
    '''convert local datetime to utc datetime

    :param local_st: datetime.datetime type
    :return:
    '''
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


