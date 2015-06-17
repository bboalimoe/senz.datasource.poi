__author__ = 'wuzhifan'

from SenzPoi.senz.tests.base import TestBase


class TestControllerManager(TestBase):
    '''test workflow from view to manager via controller and pipeline

    '''
    URL_BASE = '/senz/places/'

    def __init__(self):
        super(TestControllerManager, self).__init__()
        self.headers = {"Content-type":"application/json"}

    def test(self, url=URL_BASE, internal=False, **kwargs):

        if internal:
            url += 'internal/'

        method = 'POST'
        params = {}
        if 'args' in kwargs:
            params = kwargs['args']
        return self.testBase(params, method, url, self.headers)


def test_place_recognition(internal=False):
    testor = TestControllerManager()
    args = {
        'user_id' : 'hello world',
        'auth_key' : 'hello world',
    }
    print testor.test(args=args, internal=internal)


if __name__ == '__main__':
    test_place_recognition(internal=True)