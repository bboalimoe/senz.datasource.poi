# -*- coding:utf-8 -*-
__author__ = 'wzf'

import logging

from SenzPoi.senz.common.controller import ControllerBase, task

LOG = logging.getLogger(__name__)


class PoiController(ControllerBase):
    def __init__(self):
        super(PoiController, self).__init__()

    @task
    def parse(self, context):
        return context['results']




