__author__ = 'bboalimoe'


import httplib
import json
#conn = httplib.HTTPConnection("120.27.30.239:9080")
conn = httplib.HTTPConnection("127.0.0.1:8000")

headers = {"Content-type":"application/json"} #application/x-www-form-urlencoded
params = {

"userId": "adsfadfadsf",
"locGPS": [ {
"latitude": 54,
"longitude": 123,
"timestamp": 12234325345
}],
"locBeacon": [ {
"uuid": "adfad",
"major": "adfaljdfla",
"minor":"adfadsf",
"rssi": 150,
"timestamp": 123123434
}]
}


conn.request("POST", "/senz/poi_Gpeacon/", json.JSONEncoder().encode(params), headers)
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