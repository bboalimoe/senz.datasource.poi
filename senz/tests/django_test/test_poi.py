__author__ = 'wuzhifan'

import json

from . import base

class TestPoi(base.SenzTestBase):
    def test_get_places(self):
        content_type = 'application/json;'

        url = '/senz/pois/'

        params = json.dumps({
            'locations' : [{'timestamp': 1427642632501L,
                             'location': {'latitude': 39.96957,
                                            '__type': u'GeoPoint',
                                            'longitude': 116.391648}}]
            })
        response = self.client.post(url, params, content_type=content_type)

        self.assertEqual(response.status_code, 200)

        pois = json.loads(response.content)

        self.assertIn('pois', pois['results']['parse_poi'][0])
        self.assertGreater(len(pois['results']['parse_poi'][0]), 0)