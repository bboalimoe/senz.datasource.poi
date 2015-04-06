# -*- coding:utf-8 -*-
__author__ = 'wzf'

import logging

from senz.common.controller import get_current_function_name, ControllerBase

LOG = logging.getLogger(__name__)


class PoiController(ControllerBase):
    def __init__(self):
        super(PoiController, self).__init__()

    def parse(self, context):
        job = get_current_function_name()
        pipeline = self.pipeline[job]
        return pipeline.run(context)




