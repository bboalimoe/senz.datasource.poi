__author__ = 'wzf'

import sys
import os
import json
import httplib
import logging

from senz.db.avos import avos_manager


sys.path.append(os.path.dirname(os.getcwd()))
FILE = os.getcwd()
logging.basicConfig(filename=os.path.join(FILE,'log.txt'),level=logging.INFO)

LOCAL_HOST = "127.0.0.1:8088"

TEST_HOST = "120.27.30.239:9222"

HOST_250 = '192.168.60.250:8088'

HOST_144 = '192.168.248.144:8099'

DAO_HOST = 'senz-senz-datasource-poi.daoapp.io'

class TestBase(object):
    def __init__(self):
        self.avos_manager = avos_manager.AvosManager()

    def testBase(self, params, method, url, headers):
        self.conn = httplib.HTTPConnection(DAO_HOST)
        self.conn.request(method, url,
                          json.JSONEncoder().encode(params),
                          headers)

        #print "json.JSONEncoder().encode(params)   ", \
        #                      json.JSONEncoder().encode(params)


        respon = self.conn.getresponse()
        data = respon.read()
        self.conn.close()
        return data