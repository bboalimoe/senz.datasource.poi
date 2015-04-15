__author__ = 'wzf'

import time
import json

from senz.db.avos.avos_manager import AvosManager
from senz.common.openstack import timeutils as op_timeutils
from senz.common.utils import timeutils


class TestAvos(object):
    def __init__(self):
        self.avos_manager = AvosManager()
        self.avos_class = 'UserLocation'
        self.user_pointer = {"__type": "Pointer",
                             "className": "_User",
                             "objectId": '54f189d3e4b077bf8375477d'}

    def test_get_data(self):
        raw_date = self.avos_manager.getData(self.avos_class, where='{"user": %s , "objectId" : "%s"}'%
                                                        (json.dumps(self.user_pointer), '5520dafbe4b01ae283bf0f1b'))
        date = json.loads(raw_date)['results']
        for row in date:
            print row
            print time.localtime(float(row['timestamp']) / 1000.0)
            #creatAt = timeutils.iso2timestamp(row['createdAt'])
            utc_time = op_timeutils.parse_isotime(row['createdAt'])
            local_time = timeutils.utc2local(utc_time)
            #print timeutils.utc2local(utc_time)
            #createAt = time.mktime()
            print "create At %s" % time.localtime(time.mktime(local_time.timetuple()))

    def test_get_all_data(self):
        res = self.avos_manager.getAllData(self.avos_class, where='{"user": %s}'%
                                                        json.dumps(self.user_pointer))
        for row in res:
            print row

    def test_get_users(self):
        res = self.avos_manager.getUserIdByName()

    def test_get_recent_activities(self):

        return self.avos_manager.getDateBetweenData('activities', 'start_time', '2015-04-10T13:00:00.000Z', '2015-04-13T13:00:00.000Z')

if __name__ == '__main__':
    test = TestAvos()
    #test.test_get_all_data()
    res = json.loads(test.test_get_recent_activities())['results']
    print len(res)
    print res
    #'{"start_time":{"$gte":{"__type":"Date","iso":"2015-04-10T13:00:00.000Z"},"$lte":{"__type":"Date","iso":"2015-04-13T13:00:00.000Z"}}}'



