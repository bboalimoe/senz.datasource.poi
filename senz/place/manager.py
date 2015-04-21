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
        pass

    def place_recognition(self, user_id, auth_key, user_trace):
        pass
