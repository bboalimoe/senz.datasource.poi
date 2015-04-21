__author__ = 'wzf'

import logging

from senz.common.controller import ControllerBase, task

LOG = logging.getLogger(__name__)

class PlaceController(ControllerBase):
    def __init__(self):
        super(PlaceController, self).__init__()

    @task
    def place_recognition(self, context):
        return context['results']

    @task
    def internal_place_recognition(self, context):
        return context['results']
