from senz.common.utils import geoutils

__author__ = 'wzf'

import logging
import json

from senz.common.manager import ManagerBase
from senz.exceptions import *
from senz.common.utils import geoutils
from senz.place.LocationRecognition import LocationRecognition
from senz.db.avos.avos_manager import AvosManager
from senz.db.resource import user
from senz.db.avos.avos import AVObject

LOG = logging.getLogger(__name__)


class StoreBackend(object):
    pass


EXTERNAL_USER_CLASS = '_User'
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

    # def _merge_trace(self, user_pointer, request_trace, old_trace):
    def _merge_trace(self, user_pointer, request_trace, old_trace):
        ''' if internal place recognition need store trace, this method should be refactoring !!!!!!
        '''
        temp_trace_dict = {}
        for p in old_trace:
            timestamp = user.get_trace_timestamp(p)

            if timestamp not in temp_trace_dict:
                temp_trace_dict[timestamp] = p
            # raise exception if same timestamp have different geo point
            elif not geoutils.is_same_location(p['location']['longitude'], p['location']['latitude'],
                                               temp_trace_dict[timestamp]['location']['longitude'],
                                               temp_trace_dict[timestamp]['location']['latitude']):
                raise SenzExcption(msg="Duplicated geo point with same timestamp.")

        new_trace = []
        for p in request_trace:
            timestamp = user.get_trace_timestamp(p)

            if timestamp not in temp_trace_dict:
                p['user'] = user_pointer
                new_trace.append(dict(location=p['location'], timestamp=timestamp, user=user_pointer))



            else:
                old = temp_trace_dict[timestamp]
                if not geoutils.is_same_location(p['location']['longitude'], p['location']['latitude'],
                                                 old['location']['longitude'], old['location']['latitude']):
                    raise SenzExcption(msg="Duplicated geo point with same timestamp.")


        # print "new trace %s" % new_trace
        self.avos_manager.saveData(EXTERNAL_USER_TRACE_CLASS, new_trace)

        return new_trace + old_trace


    # def place_recognition(self, context, external_user, dev_key, user_trace):
    def place_recognition(self, context, userId, dev_key, user_trace):
        ''' external service api
        find user and prepare trace data, then use LocationRecognition to cluster
        :param context:
        :param external_user:
        :param dev_key:
        :param user_trace:
        :return:
        '''

        # raw = self.avos_manager.getData(EXTERNAL_USER_CLASS, where='{"objectId":"%s"}'
        #                                                            % (userId))

        raw = self.avos_manager.getData(EXTERNAL_USER_CLASS, where={"objectId": userId})
        user = json.loads(raw)['results']
        user_pointer = {"__type": "Pointer", "className": "_User", "objectId": userId}

        if user:
            old_trace = self.avos_manager.getAllData(EXTERNAL_USER_TRACE_CLASS,
                                                     where='{"user":%s}' % json.dumps(user_pointer))
        else:
            raise Exception('no user found under userId:', userId)

        prepared_trace = self._merge_trace(user_pointer, user_trace, old_trace)

        return self.handler.startCluster(user_pointer['objectId'], 'place', prepared_trace)

    def internal_place_recognition(self, context, user_id):
        print "in place manager place recognition %s" % user_id

        return self.handler.startCluster(user_id)


# userId = u"5593ef24e4b0001a928fa39a"
# avm = AvosManager()

# result = avm.getData("_User", where={"objectId": userId})
# print 'result:', result
# avObject = AVObject()
# x = avObject.get(userId)
# print x