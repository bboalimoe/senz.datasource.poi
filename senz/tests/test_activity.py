__author__ = 'wzf'

from base import TestBase

class TestActivity(TestBase):
    def __init__(self):
        super(TestActivity, self).__init__()
        self.headers = {"Content-type":"application/json"}

    def get_data(self, user_id):
        gpsList = self.avos_manager.getAllData('UserLocation', where='{"userId":"%s"}' % user_id)
        return gpsList

    def test_activity_mapping(self, user_trace, last_days):
        url = '/senz/activities/mapping/'
        method = 'POST'
        params = {
            'user_trace' : user_trace,
            'last_days' : last_days,
        }
        return self.testBase(params, method, url, self.headers)

if __name__ == '__main__':
    users = { #'zhushixiang' : '550e7481e4b01608684b3f8e',
              #'zhanghengyang' : '54f6df98e4b0c976f0300c00',
              'hihell' : '54f189d3e4b077bf8375477d',
              #'gynsolomon' : '550d34b6e4b0e3088f6a1fa5',
              #'fxp008' : '54f17f8ae4b077bf8374b015',
              #'fxp007' : '54f17f60e4b077bf8374adeb',
              #'bboalimoe' : '54f935fde4b06c41dfde8ae8',
              #'meowoodie' : '54f190fde4b077bf8375ac60',
    }
    testor = TestActivity()

    for u in users:
        user_trace = testor.get_data(users[u])
        print testor.test_activity_mapping(user_trace, 3)
    #testor.testAddNearTag()