# -*- coding: utf-8 -*-
from senz.common.utils import timeutils

__author__ = 'wzf'

import time
import json

from senz.common.openstack import timeutils as op_timeutils
from senz.common.utils import timeutils
from senz.db.avos.avos_manager import AvosManager
from senz.exceptions import *


USER_TRACE_PROJECT = 'life_logger'

TRACE_CLASS = 'UserLocation'

def get_trace_timestamp(trace_point):
    if 'timestamp' in trace_point:
        timestamp = trace_point['timestamp']
    else:
        utc_time = op_timeutils.parse_isotime(trace_point['createdAt'])
        local_time = timeutils.utc2local(utc_time)
        #'timestamp' should be unit by second
        timestamp = time.mktime(local_time.timetuple()) * 1000
        trace_point['timestamp'] = timestamp

    return timestamp

class UserTrace(object):
    def __init__(self):
        self.avos_manager = AvosManager()

    def _transform_trace(self, raw_data):
        ''' format trace dicts

        Some kind of trace data should be transformed like UserLocation in 'lifelogger' project
        :param raw_data:
        :return:
        '''
        results = []
        for row in raw_data:
            timestamp = get_trace_timestamp(row)

            #print row
            #print timestamp
            results.append(dict(objectId=row['objectId'], timestamp=timestamp,
                                longitude=row['location']['longitude'],
                                latitude=row['location']['latitude'],
                                userId=row['user']))

        return results

    def get_user_trace(self, user_id):
        '''get user trace from class 'UserLocation' of 'lifelogger' project in leancloud.

        It will drop trace data of weekend
        '''
        avos_class = TRACE_CLASS
        user_pointer = {"__type": "Pointer", "className": "_User","objectId": user_id}
        raw_data = self.avos_manager.getAllData(avos_class, where='{"user": %s }'% json.dumps(user_pointer))
        results = []
        return self._transform_trace(raw_data)


    def get_trace_users(self):
        try:
            res = self.avos_manager.get_users(USER_TRACE_PROJECT)
        except AvosCRUDError, e:
            return []


    def get_user_recent_trace(self, user_id, last_days):
        print 'Getting user trace list ...'
        L = 200
        start = 0
        res_len = L
        locations = []
        user_pointer = {"__type": "Pointer", "className": "_User","objectId": user_id}
        while res_len == L:
            res = json.loads( self.avos_manager.getDateBetweenData(TRACE_CLASS,
                                                                  "createdAt",
                                                                  timeutils.DaysBeforeAvosDate(last_days),
                                                                  timeutils.nowAvosDate(),
                                                                  where='{"user": %s }'% json.dumps(user_pointer),
                                                                  limit=L,
                                                                  skip=start))['results']
            res_len = len(res)

            print "get %d user trace" % res_len
            for loc in res:
                locations.append(loc)
            start = start+L

        return self._transform_trace(locations)


    def getUserData(self, userId):
        '''
        deprecated

        :param userId:
        :return:
        '''

        avosClass = 'UserLocationTrace'
        jsonArray = self.avos_manager.getAllData(avosClass, where='{"userId":"%s"}'% userId)

        #print jsonArray
        #print "get %d date" % len(jsonArray)
        print 'Done'

        return jsonArray
