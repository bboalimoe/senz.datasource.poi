# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

from senz.common.manager import ManagerBase


def _parseGpsPoi(poiGetor, gps,timestamped_dict, rt):
        #LOG.info('start parse gps %s' % gps)
        results = poiGetor.parsePoi(gps["latitude"], gps["longitude"])
        #LOG.info('parse results %s' % results)

        #print "results", results
        if not results:
            return
        poiType, poiName = results['poiType'], results['name']
        rt.setdefault("poiType",poiType)
        rt.setdefault("locDescription",poiName)  #poiname => locDescription
        timestamp_ = gps['timestamp']
        rt.setdefault("timestamp", timestamp_)


        if timestamp_ in timestamped_dict.keys():
            rt.setdefault("actiType",timestamped_dict[str(timestamp_)]["category"])
            rt.setdefault("actiName",timestamped_dict[str(timestamp_)]["name"])

            rt.setdefault("actiDescription",timestamped_dict[str(timestamp_)]["region"])
            rt.setdefault("actiStartTime",timestamped_dict[str(timestamp_)]["start_time"])
            rt.setdefault("actiEndTime",timestamped_dict[str(timestamp_)]["end_time"])


class ActivityManager(ManagerBase):
    def __init__(self):
        super(ActivityManager, self).__init__()

    def activity_mapping(self, context, gps, user_id):
        pass