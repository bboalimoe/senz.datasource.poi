__author__ = 'wzf'

import logging

from senz.common.manager import ManagerBase
from senz.exceptions import error_info

LOG = logging.getLogger(__name__)

class PlaceManager(ManagerBase):
    def __init__(self, pipeline, task_name):
        super(PlaceManager, self).__init__(pipeline, task_name)

    def store_raw(self, raw):
        pass

    def store_results(self, results):
        pass

    def store(self, context):
        print "in place manager store"

    def place_recognition(self, user, auth_key, user_trace):
        print "in place manager place recognition " % user , auth_key, user_trace

    def internal_place_recognition(self, user_id):
        print "in place manager place recognition" % user_id