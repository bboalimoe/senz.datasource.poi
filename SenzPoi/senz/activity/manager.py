# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.manager import ManagerBase
from senz.activity.UserActivityMapping import UserActivityMapping
import json
from senz.db.avos.avos_manager import *
from senz.common.utils import timeutils


class ActivityManager(ManagerBase):
    def __init__(self, *args, **kwargs):
        super(ActivityManager, self).__init__(*args, **kwargs)
        self.avos_manager = AvosManager()

    def _update_gps(self, mapping_timestamp, user_trace):
        for g in user_trace:
            timestamp_ = g['timestamp']
            if mapping_timestamp and timestamp_ in mapping_timestamp.keys():
                g.setdefault("act_type", mapping_timestamp[str(timestamp_)]["category"])
                g.setdefault("act_name", mapping_timestamp[str(timestamp_)]["name"])

                g.setdefault("act_description", mapping_timestamp[str(timestamp_)]["region"])
                g.setdefault("act_startTime", mapping_timestamp[str(timestamp_)]["start_time"])
                g.setdefault("act_endTime", mapping_timestamp[str(timestamp_)]["end_time"])

    def activity_mapping(self, context, user_trace, user_id=None, last_days=3):
        handler = UserActivityMapping()
        mapping_timestamp = handler.map_user_activity(user_id, user_trace, last_days)

        self._update_gps(mapping_timestamp, user_trace)
        return mapping_timestamp

    def home_office_status(self, context, userId, geo_point, timestamp):
        handler = UserActivityMapping()

        timestamp = timestamp/1000 # make timestamp to standard timestamp

        user_pointer = {"__type": "Pointer", "className": "_User", "objectId": userId}
        places = self.avos_manager.getAllData('place', where='{"user": %s }' % json.dumps(user_pointer))

        place_home = None
        place_office = None

        for place in places:
            if 'home' == place['tag']:
                place_home = place
            elif 'office' == place['tag']:
                place_office = place

        if not timeutils.is_weekday(timestamp):
            raise Exception('timestamp is not local weekday, can not analysis home office intention, timestamp:',
                            timestamp)

        if place_home and place_office:
            status = handler.home_office_status(place_home, place_office, geo_point, timestamp)
            return status
        else:
            raise Exception('not enough data for home office intention analysis, userId:', userId)
