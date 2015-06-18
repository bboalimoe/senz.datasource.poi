__author__ = 'wuzhifan'

import logging

from senz.common.controller import ControllerBase, task

LOG = logging.getLogger(__name__)

class ActivityController(ControllerBase):
    def __init__(self):
        super(ActivityController, self).__init__()

    @task
    def activity_mapping(self, context):
        print "in controller activity mapping"
        return context['results']


