# -*- coding:utf-8 -*-
__author__ = 'wzf'

import logging
import time

import threadpool

from senz.poi.poi import PoiGet
from senz.activity.UserActivityMapping import UserActivityMapping

from senz.common import settings
from senz.common.controller import get_current_function_name, ControllerBase

from senz.common.filter import FilterBase
from senz.exceptions import *


LOG = logging.getLogger(__name__)




class PoiController(ControllerBase):
    def __init__(self):
        super(PoiController, self).__init__()

    def parse(self, context):
        job = get_current_function_name()
        pipeline = self.pipeline[job]
        return pipeline.run(context)






