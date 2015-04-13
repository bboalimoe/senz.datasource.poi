__author__ = 'wzf'

from base import TestBase

class TestPlaceApi(TestBase):
    def __init__(self):
        super(TestPlaceApi, self).__init__()
        self.headers = {"Content-type":"application/json"}
        #self.destUserId = "54f6df98e4b0c976f0300c00"

    def testLocTag(self, user_id, sampling_interval=600, time_threshold=1800):
        url = '/senz/places/'
        method = 'POST'
        params = {
            'user_id' : user_id,
            'sampling_interval' : sampling_interval,
            'time_threshold' : time_threshold,
        }
        return self.testBase(params, method, url, self.headers)

    def testAddNearTag(self):
        url = '/senz/places/user/' + self.destUserId + '/tag/'
        method = 'GET'

        self.testBase({}, method, url, self.headers)


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
    testor = TestPlaceApi()
    for user in users:
        print testor.testLocTag(users[user])
    #testor.testAddNearTag()
