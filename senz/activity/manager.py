# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.manager import ManagerBase
from senz.activity.UserActivityMapping import UserActivityMapping

class ActivityManager(ManagerBase):
    def __init__(self):
        super(ActivityManager, self).__init__()

    def _update_gps(self, mapping_timestamp, user_trace):
        for g in user_trace:
            timestamp_ = g['timestamp']
            if timestamp_ in mapping_timestamp.keys():
                g.setdefault("act_type",mapping_timestamp[str(timestamp_)]["category"])
                g.setdefault("act_name",mapping_timestamp[str(timestamp_)]["name"])

                g.setdefault("act_description",mapping_timestamp[str(timestamp_)]["region"])
                g.setdefault("act_startTime",mapping_timestamp[str(timestamp_)]["start_time"])
                g.setdefault("act_endTime",mapping_timestamp[str(timestamp_)]["end_time"])

    def activity_mapping(self, context, user_trace, user_id):
        handler = UserActivityMapping()
        mapping_timestamp = handler.mapActivityByUser(user_id, user_trace)

        self._update_gps(mapping_timestamp, user_trace)
        return mapping_timestamp