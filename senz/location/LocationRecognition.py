# -*- encoding=utf-8 -*-
import logging
import datetime

import scipy.cluster.hierarchy as sch

from senz.common.avos.avos_manager import *
from senz.common.utils.geoutils import LocationAndTime, coordArrayCompress, distance
from senz.common.utils.clusterutils import filterClustersBySize
from senz.common.utils import timeutils


# params
LOG = logging.getLogger(__name__)

DEFAULT_TIME_RANGES = [[22, 23, 0, 1, 2, 3, 4, 5, 6, 7], [9, 10, 11, 14, 15, 16, 17]]
DEFAULT_TAG_OF_TIME_RANGES = ["home", "office"]
version = '0.1'


# data structure

class LocationWithTags:
    """Location from cluster result and tags by analysing timestamps"""

    def __init__(self, _latitude, _longitude, _tags):
        self.latitude = _latitude
        self.longitude = _longitude
        self.tags = _tags
        self.estimateTime = 0

class TagInfo:
    def __init__(self, _tag, _estimateTime, _ratio):
        self.tag = _tag
        self.estimateTime = _estimateTime
        self.ratio = _ratio

class LocationRecognition(object):
    def __init__(self):
        self.avosManager = AvosManager()

    def cluster(self, jsonArray, maxClusterRadius=0.00125, samplingInteval=10000,
                           timeRanges=DEFAULT_TIME_RANGES, tagOfTimeRanges=DEFAULT_TAG_OF_TIME_RANGES, timeThreshold = 300000,
                           ratioThreshold = 0.4):

        LOG.info("start place cluster.")

        # parse json data

        rawDataArray = []
        for jsonRecord in jsonArray:
            #print "jsonRecord",jsonRecord
            rawDataArray.append(LocationAndTime(jsonRecord["timestamp"], jsonRecord["latitude"], jsonRecord["longitude"]))
            #rawDataArray.append(LocationAndTime(jsonRecord["time"], jsonRecord["lat"], jsonRecord["lon"]))

        # print("%d records" % len(rawDataArray))

        # sampling by time

        rawDataArray.sort(key=LocationAndTime.time)

        dataArray = coordArrayCompress(rawDataArray, samplingInteval)

        print("%d standardized records" % len(dataArray))
        if len(dataArray) <= 1:
            LOG.warning("Not enough data in clustering place data!")
            return []

        # clustering

        positionArray = []
        for data in dataArray:
            positionArray.append([data.latitude, data.longitude])

        distanceMatrix = sch.distance.pdist(positionArray)

        #对位置信息做聚类
        linkageMatrix = sch.linkage(positionArray, method='centroid', metric='euclidean')
        # Z矩阵：第 i 次循环是第 i 行，这一次[0][1]合并了，它们的距离是[2]，这个类簇大小为[3]

        clusterResult = sch.fcluster(linkageMatrix, maxClusterRadius, 'distance')

        print("%d clusters" % clusterResult.max())

        # filter clusters
        validCluster = filterClustersBySize(clusterResult, dataArray, timeThreshold / samplingInteval)

        # add tags

        globalDataInRangeCount = self.countDataInRange(dataArray, timeRanges)

        results = []
        print validCluster
        for cluster in validCluster:
            clusterDataInRangeCount = self.countDataInRange(cluster, timeRanges)

            tags = []
            i = 0
            while i < len(timeRanges):
                if globalDataInRangeCount[i] == 0:
                    i += 1
                    continue
                ratio = float(clusterDataInRangeCount[i]) / globalDataInRangeCount[i]
                print ratio
                if ratio > ratioThreshold:
                    estimateTime = clusterDataInRangeCount[i] * samplingInteval    #todo: estimateTime is point count multi interval??????
                    tags.append(TagInfo(tagOfTimeRanges[i], estimateTime, ratio))
                i += 1

            if len(tags) == 0:  # no tag
                continue

            sumLa = 0
            sumLo = 0
            count = 0

            for data in cluster:
                sumLa += data.latitude
                sumLo += data.longitude
                count += 1

            avgLa = sumLa / count
            print "avgLa", avgLa
            avgLo = sumLo / count

            result = LocationWithTags(avgLa, avgLo, tags)
            result.estimateTime = count * samplingInteval
            print ("r",results)
            results.append(result)
        print (results)

        print "return cluster results : %d" % len(results)
        # output are in results
        return results

    def countDataInRange(self,dataArray, timeRanges):

        dataInRangeCount = [0] * len(timeRanges)
        for data in dataArray:
            timeStamp = time.localtime(data.time / 1000)
            i = 0
            while i < len(timeRanges):
                if timeStamp.tm_hour in timeRanges[i]:
                    dataInRangeCount[i] += 1
                i += 1
        return dataInRangeCount

    def startCluster(self, userId=None):

        try:
            #return old place recognition data if it generated in 7 days
            locRecgClass = 'LocationRecognition'

            oldLocRecgData = json.loads(self.avosManager.getData(
                                   locRecgClass,
                                   where='{"userId":"%s"}'% userId ))['results']

            if len(oldLocRecgData) > 0:
                #createDate = timeutils.ISOString2Time(oldLocRecgData[0]['createdAt'],
                #                                      timeutils.ISO_TIME_FORMAT)

                createDate = datetime.datetime.strptime(oldLocRecgData[0]['createdAt'],
                                                        timeutils.ISO_TIME_FORMAT)

                nowDate = datetime.datetime.now()
                if (nowDate - createDate).days < 7:
                    return oldLocRecgData
                else:
                    #if recgData out of date then delete it
                    for recgData in oldLocRecgData:
                        self.avosManager.deleteData(locRecgClass, recgData)


            data = self.getData(userId)

            results = self.cluster(data)

            if len(results) > 0:
                self.saveResults(results, userId)

            return json.dumps(results,default=lambda obj:obj.__dict__)
        except Exception as e:
            LOG.error("exception in place clustering : %s" % e.message)
            raise e




    def saveResults(self, results, userId=None):
        #save place recgnition results to leancloud
        avosClassName = 'LocationRecognition'
        for result in results:
            for tag in result.tags:
                self.avosManager.saveData(avosClassName,{"latitude":result.latitude,
                                                                    "longitude":result.longitude,
                                                                    "tag":tag.tag,
                                                                    "ratio":tag.ratio,
                                                                    "estimateTime":result.estimateTime,
                                                                    "userId":userId,
                                                                    "date": "",
                                                                    "status": ""})


    def addNearTags(self, userId):
        '''add tags near to user trace data points

           this method will overlap old near tags
        '''

        traceClass = 'UserLocationTrace'
        locRecgClass = 'LocationRecognition'
        nearDistance = 200

        traceData = self.avosManager.getAllData(traceClass,  where='{"userId":"%s"}'% userId)

        locRecgData = json.loads(self.avosManager.getData(
                                   locRecgClass,
                                   where='{"userId":"%s"}'% userId ))['results']

        for trace in traceData:
            trace['near'] = []
            for locRecg in locRecgData:
                if distance(trace['longitude'], trace['latitude'],
                             locRecg['longitude'], locRecg['latitude']) < nearDistance:
                    if locRecg['tag'] not in trace['near']:
                        trace['near'].append(locRecg['tag'])

        LOG.info("add near tag to %d trace data" % len(traceData))

        res = self.avosManager.updateDataList(traceClass, traceData)
        #for trace in traceData:
        #    self.avosManager.updateDataById(traceClass,trace['objectId'], {'near' : str(trace['near']) })




    def getData(self, userid=None):

        if not userid:
            print "shit"
            file = open("testLocation.json")
            jsonArray = json.load(file)["results"]

        else:
            jsonArray = self.getUserData(userid)


        return jsonArray



    def getUserData(self, userId):

        lean = AvosManager()
        avosClass = 'UserLocationTrace'
        jsonArray = lean.getAllData(avosClass, where='{"userId":"%s"}'% userId)

        print jsonArray
        print "get %d date" % len(jsonArray)
        print 'Done'

        return jsonArray
        #result = lean.saveData("UserLocationTrace",{"latitude":gps['latitude'],"longitude":gps["longitude"],"activityId":"", "timpstamp":gps['timestamp'],"userId":userId})



if __name__ == '__main__':
    '''
    #transfer user trace from location_record class to UserLocationTrace
    avosManager = AvosManager()
    userId = '2b4e710aab89f6c5'

    L = 200
    start = 0
    res_len = L
    jsonArray = []
    while res_len == L:
        res = json.loads(avosManager.getData('location_record',limit=L, skip=start, where='{"userId":"%s"}'% userId ))['results']
        res_len = len(res)
        for location_record in res:
            jsonArray.append(location_record)
        start = start+L
    #baseData = json.loads(avosManager.getData('location_record', where='{"userId": "%s"}' % userId))['results']

    for row in jsonArray:
        result = avosManager.saveData('UserLocationTrace',{
                                                       "latitude":row['latitude'],"longitude":row["longitude"],
                                                       "activityId":"", "timestamp":row['timestamp'],
                                                       "near":"", "userId":userId})

    '''

    '''
    lean = AvosManager()
    res = json.loads(lean.getData('UserLocationTrace', limit=1000, skip=0))['results']
    print len(res)
    print res
    '''

    obj = LocationRecognition()
    #print obj.startCluster("54d82fefe4b0d414801050ee")
    #print obj.startCluster("")
    print obj.startCluster("2b4e710aab89f6c5")
