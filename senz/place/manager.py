__author__ = 'wzf'

import logging
import json
from senz.common.manager import ManagerBase
from senz.exceptions import *
from senz.common.utils import geoutils
from senz.place.LocationRecognition import LocationRecognition
from senz.db.avos.avos_manager import AvosManager


LOG = logging.getLogger(__name__)


class StoreBackend(object):
    pass


EXTERNAL_USER_CLASS = 'users'
EXTERNAL_USER_TRACE_CLASS = 'user_trace'

class PlaceManager(ManagerBase):
    def __init__(self, pipeline, task_detail):
        super(PlaceManager, self).__init__(pipeline, task_detail)
        self.handler = LocationRecognition()
        self.avos_manager = AvosManager()

    def store_raw(self, raw):
        pass

    def store_results(self, results):
        pass

    def store(self, context):
        '''not implemented
        '''
        print "in place manager store"

    def _merge_trace(self, user_pointer, request_trace, old_trace):
        ''' if internal place recognition need store trace, this method should be refactoring !!!!!!

        '''
        temp_trace_dict = {}
        for p in old_trace:
            if p['timestamp'] not in temp_trace_dict:
                temp_trace_dict[p['timestamp']] = p
            else:
                raise SenzExcption("Duplicated geo point with same timestamp.")

        new_trace = []
        for p in request_trace:
            if p['timestamp'] not in temp_trace_dict:
                p['user'] = user_pointer
                new_trace.append(p)
            else:
                old = temp_trace_dict[p['timestamp']]
                if not geoutils.is_same_location(p['location']['longitude'], p['location']['latitude'],
                                                    old['location']['longitude'], old['location']['latitude']):
                    raise SenzExcption("Duplicated geo point with same timestamp.")

        self.avos_manager.saveData(EXTERNAL_USER_TRACE_CLASS, new_trace)


        return new_trace + old_trace


    def place_recognition(self, context, external_user, dev_key, user_trace):
        print "in place manager place recognition %s, %s, %s" % (external_user, dev_key, user_trace)

        raw = self.avos_manager.getData(EXTERNAL_USER_CLASS, where='{"external_user":"%s", "dev_key":"%s"}'
                                                 % (external_user, dev_key))
        user = json.loads(raw)['results']
        user_pointer = {"__type": "Pointer", "className": "users", "objectId": None}
        if user:
            user_pointer['objectId'] = user[0]['objectId']
            old_trace = self.avos_manager.getAllData(EXTERNAL_USER_TRACE_CLASS, where='{"user":%s}' % json.dumps(user_pointer))
        else:
            user = json.loads(self.avos_manager.saveData(EXTERNAL_USER_CLASS,
                                                dict(external_user=external_user,dev_key=dev_key)))['results']
            user_pointer['objectId'] = user[0]['objectId']
            old_trace = []

        prepared_trace = self._merge_trace(external_user, dev_key, user_trace)

        return self.handler.startCluster(user_pointer['objectId'], 'place', prepared_trace)



    def internal_place_recognition(self, context, user_id):
        print "in place manager place recognition %s" % user_id

        return self.handler.startCluster(user_id)