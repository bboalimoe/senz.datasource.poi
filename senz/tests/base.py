__author__ = 'wzf'

import sys, os
import json
import httplib
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
FILE = os.getcwd()
logging.basicConfig(filename=os.path.join(FILE,'log.txt'),level=logging.INFO)

TEST_HOST = "127.0.0.1:8088"

class TestBase(object):
    def __init__(self):
        pass

    def testBase(self, params, method, url):
        self.conn = httplib.HTTPConnection(TEST_HOST)
        self.conn.request(method, url,
                          json.JSONEncoder().encode(params),
                          self.headers)

        print "json.JSONEncoder().encode(params)   ", \
                              json.JSONEncoder().encode(params)


        respon = self.conn.getresponse()
        data = respon.read()
        print data

        self.conn.close()