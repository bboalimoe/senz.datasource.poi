__author__ = 'wuzhifan'

import json

from SenzPoi.senz.tests.django_test import base


class TestPoi(base.SenzTestBase):
    def _get_test_user_trace(self):
        user_pointer = {"__type": "Pointer",
                        "className": "_User",
                        "objectId": "54f189d3e4b077bf8375477d"}

        gpslist = self.avos_manager.getAllData('UserLocation',
                                where='{"user":%s}' % json.dumps(user_pointer))    #Warning:DataSample UserLocation

        return gpslist

    def test_get_places(self):
        content_type = 'application/json;'

        url = '/senz/places/'

        user_trace = self._get_test_user_trace()

        params = json.dumps({
                 'external_user' : 'jiusi',
                 'dev_key' : 'wzf',
                 'user_trace' : user_trace,
            })

        response = self.client.post(url, params, content_type=content_type)

        self.assertEqual(response.status_code, 200)

        pois = json.loads(response.content)

        self.assertGreater(len(pois['results']['place_recognition']), 0)