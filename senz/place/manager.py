__author__ = 'wzf'

import logging

from senz.common.manager import ManagerBase
from senz.exceptions import error_info

from senz.place.LocationRecognition import LocationRecognition

LOG = logging.getLogger(__name__)


class StoreBackend(object):
    pass

class PlaceManager(ManagerBase):
    def __init__(self, pipeline, task_detail):
        super(PlaceManager, self).__init__(pipeline, task_detail)
        self.handler = LocationRecognition()

    def store_raw(self, raw):
        pass

    def store_results(self, results):
        pass

    def store(self, context):
        print "in place manager store"

    def place_recognition(self, context, external_user, dev_key, user_trace):
        print "in place manager place recognition %s, %s, %s" % (external_user, dev_key, user_trace)



    def internal_place_recognition(self, context, user_id):
        print "in place manager place recognition %s" % user_id

        return self.handler.startCluster(user_id)