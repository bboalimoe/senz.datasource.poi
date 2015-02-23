__author__ = 'bboalimoe'


import httplib
import json
conn = httplib.HTTPConnection("120.27.30.239:9080")
#conn = httplib.HTTPConnection("localhost:8000")

headers = {"Content-type":"application/json"} #application/x-www-form-urlencoded
params = {

            "lat": "40.056885091681",
            "lng": "116.30814954222",
    }

conn.request("POST", "/senz/get_baidu_poitype/", json.JSONEncoder().encode(params), headers)
print "json.JSONEncoder().encode(params)   ", json.JSONEncoder().encode(params)
response = conn.getresponse()
data = response.read()
print data
"""
if response.status == 200:
    print 'success'
    print data
else:
    print 'fail'
"""
conn.close() 