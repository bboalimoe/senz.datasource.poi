__author__ = 'wuzhifan'

import json
import time, datetime
from base import TestBase

from senz.common.openstack import timeutils as op_timeutils
from senz.common.utils import timeutils

from senz.db.avos.avos_manager import AvosManager
class TestTime(TestBase):
    def __init__(self):
        super(TestTime, self).__init__()
        self.avos_manager = AvosManager()

    def test_time(self):
        avos_class = 'UserLocation'
        object_id = '5520910ce4b01ae283bb635f'
        user_id = '54f189d3e4b077bf8375477d'
        user_pointer = {"__type": "Pointer", "className": "_User","objectId": user_id}
        raw_data = self.avos_manager.getAllData(avos_class, where='{"user": %s , "objectId": "%s"}'
                                                                  % (json.dumps(user_pointer),
                                                                      object_id))
        print raw_data

        for row in raw_data:
            timestamp = time.localtime(row['timestamp'] / 1000)
            print "timestamp : %d ------ %s " % (row['timestamp'], timestamp)
            utc_time = op_timeutils.parse_isotime(row['createdAt'])
            local_time = timeutils.utc2local(utc_time)
            creat_at_timestamp = time.mktime(local_time.timetuple())
            print "create at : %d ------ %s " % (creat_at_timestamp, local_time)


if __name__ == '__main__':
    test = TestTime()
    test.test_time()