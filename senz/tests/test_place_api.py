__author__ = 'wzf'

from base import TestBase

from senz.db.avos.avos_manager import AvosManager

class TestPlaceApi(TestBase):
    def __init__(self):
        super(TestPlaceApi, self).__init__()
        self.headers = {"Content-type":"application/json"}
        #self.destUserId = "54f6df98e4b0c976f0300c00"
        self.avos_manager = AvosManager()

    def testLocTag(self, user_id, sampling_interval=600, time_threshold=1800):
        url = '/senz/places/'
        method = 'POST'
        params = {
            'user_id' : user_id,
            'sampling_interval' : sampling_interval,
            'time_threshold' : time_threshold,
        }
        return self.testBase(params, method, url, self.headers)

    def test_internal_place_recognition(self, user_id, user_trace):
        url = '/senz/places/internal/'
        method = 'POST'
        params = {
            'user_id' : user_id,
            'user_trace' : user_trace,
        }

        return self.testBase(params, method, url, self.headers)

    def testAddNearTag(self):
        url = '/senz/places/user/' + self.destUserId + '/tag/'
        method = 'GET'

        self.testBase({}, method, url, self.headers)


if __name__ == '__main__':
    testor = TestPlaceApi()

    avos_manager = AvosManager()
    gpslist = avos_manager.getAllData('UserLocation')

    clean_data = {}
    for g in gpslist:
        if g['installation'] in clean_data:

            dest = clean_data[g['installation']]

        else:

            dest = []
            clean_data[g['installation']] = dest

        dest.append(dict(timestamp = g['timestamp'] / 1000,
                           latitude=g['location']['latitude'],
                           longitude=g['location']['longitude']))

    #print len(clean_data)
    for user_install_id in clean_data:
        if len(clean_data[user_install_id]) < 10:
            continue

        if len(clean_data[user_install_id]) > 300:
            copy = []
            for d in clean_data[user_install_id]:
                copy.append([d['longitude'], d['latitude']])

            print copy



            #print clean_data[user_install_id]
            print user_install_id
            print len(clean_data[user_install_id])
            res = testor.test_internal_place_recognition(user_install_id, clean_data[user_install_id])
            print res


    '''
    users = { #'zhushixiang' : '550e7481e4b01608684b3f8e',
              #'zhanghengyang' : '54f6df98e4b0c976f0300c00',
              'hihell' : '54f189d3e4b077bf8375477d',
              #'gynsolomon' : '550d34b6e4b0e3088f6a1fa5',
              #'fxp008' : '54f17f8ae4b077bf8374b015',
              #'fxp007' : '54f17f60e4b077bf8374adeb',
              #'bboalimoe' : '54f935fde4b06c41dfde8ae8',
              #'meowoodie' : '54f190fde4b077bf8375ac60',
    }

    for user in users:
        print testor.testLocTag(users[user])
        '''
    #testor.testAddNearTag()
