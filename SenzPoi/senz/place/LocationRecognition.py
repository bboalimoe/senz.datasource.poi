# -*- encoding=utf-8 -*-

import scipy.cluster.hierarchy as sch

from senz.common.utils import timeutils

from senz.db.avos.avos_manager import *
from senz.common.utils.geoutils import LocationAndTime, coordArrayCompress, distance
from senz.common.utils import timeutils
from senz.exceptions import *
from senz.db.resource.user import UserTrace



# params
LOG = logging.getLogger(__name__)

DEFAULT_TIME_RANGES = [[23, 0, 1, 2, 3, 4, 5, 6, 7], [9, 10, 11, 14, 15, 16, 17]]
DEFAULT_TAG_OF_TIME_RANGES = ["home", "office"]
VERSION = '0.1'

DEFAULT_SAMPLE_INTEVAL = 600 #unit is second

DEFAULT_SAMPLE_THRESHOLD = 1800 #unit is second

DEFAULT_CLUSTER_RATIO = 0.4

DEFAULT_CLUSTER_RADIUS = 0.0125

INTERNAL_PLACE_STORE = 'LocationRecognition'

def filterClustersBySize(cluster, dataArray, size):
    allCluster = [[] for row in range(cluster.max())]

    i = 0
    while i < len(cluster):
        index = cluster[i] - 1
        allCluster[index].append(dataArray[i])  # put points to its cluster
        i += 1

    validCluster = []
    for cluster in allCluster:
        if (len(cluster) >= size):
            validCluster.append(cluster)   # filter cluster

    return validCluster


# data structure
class LocationWithTags:
    """Location from cluster result and tags by analysing timestamps"""

    def __init__(self, _latitude, _longitude, _tags, _timeStart, _timeEnd):
        self.latitude = _latitude
        self.longitude = _longitude
        self.tags = _tags
        self.timeStart = _timeStart
        self.timeEnd = _timeEnd
        self.estimateTime = 0

class TagInfo:
    def __init__(self, _tag, _estimateTime, _ratio):
        self.tag = _tag
        self.estimateTime = _estimateTime
        self.ratio = _ratio

class LocationRecognition(object):
    def __init__(self):
        self.avosManager = AvosManager()

    def cluster(self, jsonArray, maxClusterRadius=DEFAULT_CLUSTER_RADIUS, samplingInterval=DEFAULT_SAMPLE_INTEVAL,
                timeRanges=DEFAULT_TIME_RANGES, tagOfTimeRanges=DEFAULT_TAG_OF_TIME_RANGES,
                timeThreshold=DEFAULT_SAMPLE_THRESHOLD,
                ratioThreshold=DEFAULT_CLUSTER_RATIO):

        LOG.info("start place cluster.")

        # parse json data

        rawDataArray = []
        for jsonRecord in jsonArray:
            # print "jsonRecord",jsonRecord

            # make timestamp from microsecond to second facilitate computing
            timestamp = jsonRecord["timestamp"] / 1000
            if 'location' in jsonRecord:
                lng = jsonRecord['location']['longitude']
                lat = jsonRecord['location']['latitude']
            else:
                lng = jsonRecord['longitude']
                lat = jsonRecord['latitude']
            rawDataArray.append(LocationAndTime(timestamp, lat, lng))
            # rawDataArray.append(LocationAndTime(jsonRecord["time"], jsonRecord["lat"], jsonRecord["lon"]))

        # print("%d records" % len(rawDataArray))

        # sampling by time

        rawDataArray.sort(key=LocationAndTime.time)

        # compress by mean
        dataArray = coordArrayCompress(rawDataArray, samplingInterval)

        print("%d standardized records" % len(dataArray))
        if len(dataArray) <= 1:
            LOG.warning("Not enough data for places clustering!")
            raise BadRequest(resource='place',
                             msg="Not enough data for places clustering!")

        # clustering

        positionArray = []
        for data in dataArray:
            positionArray.append([data.latitude, data.longitude])

        distanceMatrix = sch.distance.pdist(positionArray)

        # 对位置信息做聚类
        # TODO understand linkage clustering
        linkageMatrix = sch.linkage(positionArray, method='centroid', metric='euclidean')
        # Z矩阵：第 i 次循环是第 i 行，这一次[0][1]合并了，它们的距离是[2]，这个类簇大小为[3]

        clusterResult = sch.fcluster(linkageMatrix, maxClusterRadius, 'distance')

        print("%d clusters" % clusterResult.max())

        # filter clusters
        validCluster = filterClustersBySize(clusterResult, dataArray, timeThreshold / samplingInterval)

        # add tags
        print "%d valid cluster" % len(validCluster)
        globalDataInRangeCount = self.countDataInRange(dataArray, timeRanges)

        # TODO understand global
        print "global : %s" % globalDataInRangeCount

        results = []
        # print validCluster
        for cluster in validCluster:

            clusterDataInRangeCount = self.countDataInRange(cluster, timeRanges)

            tags = []
            i = 0
            while i < len(timeRanges):
                if globalDataInRangeCount[i] == 0:
                    i += 1
                    continue
                ratio = float(clusterDataInRangeCount[i]) / globalDataInRangeCount[i]
                print 'ratio:', ratio
                if ratio > ratioThreshold:
                    # todo: estimateTime is point count multi interval??????
                    estimateTime = clusterDataInRangeCount[i] * samplingInterval
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
            avgLo = sumLo / count

            timeStart = -1
            timeEnd = -1
            if tags[0].tag == 'home':
                timeStart, timeEnd = self.getAvgHomeTimeRange(cluster)
            elif tags[0].tag == 'office':
                timeStart, timeEnd = self.getAvgOfficeTimeRange(cluster)

            result = LocationWithTags(avgLa, avgLo, tags, timeStart, timeEnd)
            result.estimateTime = count * samplingInterval
            results.append(result)

        print "return cluster results : %d" % len(results)
        # output are in results
        return results

    #
    def countDataInRange(self, dataArray, timeRanges):

        test_res = []

        dataInRangeCount = [0] * len(timeRanges)
        for data in dataArray:
            timeStamp = time.localtime(data.time)

            row_datetime = datetime.datetime.fromtimestamp(data.time)
            weekday = row_datetime.weekday()
            if weekday in [0, 6]:
                continue

            i = 0
            while i < len(timeRanges):
                if timeStamp.tm_hour in timeRanges[i]:
                    dataInRangeCount[i] += 1

                    # test
                    if i == 0:
                        test_res.append(dict(lat=data.latitude,
                                             lon=data.longitude,
                                             time=row_datetime.strftime(timeutils.ISO_TIME_FORMAT)))
                i += 1

        # print "day time res : %s" % test_res
        # LOG.info("day time res : %s" % test_res)
        # print "day time res len : %d" % len(test_res)
        # print "cluster len : %d" % len(dataArray)
        return dataInRangeCount

    def startCluster(self, userId, store_class=INTERNAL_PLACE_STORE, user_trace=None):
        # user_trace is "prepared trace"/"merged trace"
        # locRecgClass is "place"
        locRecgClass = store_class

        try:
            # return old place recognition data if it generated in 7 days

            user_pointer = {"__type": "Pointer", "className": "_User", "objectId": userId}
            oldLocRecgData = json.loads(self.avosManager.getData(
                locRecgClass,
                where='{"user": %s }' % json.dumps(user_pointer)))['results']
        except AvosCRUDError, e:
            LOG.warning("Get data of LocationRecognition failed.")
            oldLocRecgData = []

        try:
            if len(oldLocRecgData) > 0:
                createDate = datetime.datetime.strptime(oldLocRecgData[0]['createdAt'],
                                                        timeutils.ISO_TIME_FORMAT)


                nowDate = datetime.datetime.now()

                if (nowDate - createDate).days < 7:
                    return oldLocRecgData
                else:
                    # if recgData out of date then delete it
                    for recgData in oldLocRecgData:
                        self.avosManager.deleteData(locRecgClass, recgData)


            # data = self.getData(userId)
            if not user_trace:
                data = UserTrace().get_user_trace(userId)
            else:
                data = user_trace

            results = self.cluster(data)

            if len(results) > 0:
                # save cluster result
                transformed_res = self.saveResults(results, userId, store_class)
                return transformed_res
            else:
                return []
                # return json.dumps(results,default=lambda obj:obj.__dict__)
        except Exception as e:
            LOG.error("exception in place clustering : %s" % e.message)
            raise e

    def saveResults(self, results, userId=None, save_class=INTERNAL_PLACE_STORE, ):
        # save place recgnition results to leancloud
        avosClassName = save_class
        # transform results to suit database
        transformed_res = []
        for result in results:
            for tag in result.tags:
                user_pointer = {"__type": "Pointer", "className": "_User","objectId": userId}
                place_tag = {"location": {"latitude": result.latitude,
                                          "longitude": result.longitude,
                                          "__type": "GeoPoint"},
                             "tag": tag.tag, "ratio": tag.ratio,
                             "estimateTime": result.estimateTime, "user": user_pointer,
                             "timeStart": result.timeStart,
                             "timeEnd": result.timeEnd
                             }
                transformed_res.append(place_tag)
                self.avosManager.saveData(avosClassName, place_tag)

        return transformed_res

    def addNearTags(self, userId):
        '''add tags near to user trace data points

           this method will overlap old near tags

           deprecated
        '''
        traceClass = 'UserLocationTrace'
        locRecgClass = 'LocationRecognition'
        nearDistance = 0.2 #km

        traceData = self.avosManager.getAllData(traceClass, where='{"userId":"%s"}' % userId)

        locRecgData = json.loads(self.avosManager.getData(
            locRecgClass,
            where='{"userId":"%s"}' % userId))['results']

        for trace in traceData:
            trace['near'] = []
            for locRecg in locRecgData:
                if distance(trace['longitude'], trace['latitude'],
                            locRecg['longitude'], locRecg['latitude']) < nearDistance:
                    if locRecg['tag'] not in trace['near']:
                        trace['near'].append(locRecg['tag'])

        LOG.info("add near tag to %d trace data" % len(traceData))

        res = self.avosManager.updateDataList(traceClass, traceData)

    def getAvgHomeTimeRange(self, cluster):
        # NOTE! time in cluster is timestamp not localtime
        # NOTE! ONLY ACCEPT WEEKDAY DATA
        # ALL logic is related to local time, convert then compare

        cluster = [ele for ele in cluster if timeutils.is_weekday(ele.time)]

        morning = []
        afternoon = []

        for ele in cluster:
            local_st = timeutils.timestamp2local(ele.time)
            if local_st.hour <= 12:
                morning.append(ele)
            else:
                afternoon.append(ele)

        drop, avgEnd = self.getAvgStartEndOfCluster(morning)
        avgStart, drop = self.getAvgStartEndOfCluster(afternoon)

        return avgStart, avgEnd

    def getAvgOfficeTimeRange(self, cluster):
        cluster = [ele for ele in cluster if timeutils.is_weekday(ele.time)]
        return self.getAvgStartEndOfCluster(cluster)

    def timeOffsetToHM(self, offset):
        hour = offset / 60 / 60
        min = (offset / 60) % 60
        return hour, min

    def getAvgStartEndOfCluster(self, cluster):
        # 1 make local date bin
        timeFormat = '%Y-%m-%d'
        groupedByDate = {}

        for ele in cluster:

            local_st = timeutils.timestamp2local(ele.time)
            dateStr = local_st.strftime(timeFormat)

            if dateStr not in groupedByDate:
                groupedByDate[dateStr] = []

            groupedByDate[dateStr].append(ele)

        avgStart = 0
        avgEnd = 0

        binNumber = len(groupedByDate.keys())
        for localDate in groupedByDate.keys():
            bin = groupedByDate[localDate]
            bin.sort(key=LocationAndTime.time)

            avgStart += timeutils.secFromBeginningOfDay(bin[0].time)
            avgEnd += timeutils.secFromBeginningOfDay(bin[-1].time)

        return avgStart / binNumber, avgEnd / binNumber


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
    obj = LocationRecognition()
    #print obj.startCluster("54d82fefe4b0d414801050ee")
    #print obj.startCluster("")
    print obj.startCluster("2b4e710aab89f6c5")
    '''

    o = LocationRecognition()
    print o.get_user_trace('54f17f60e4b077bf8374adeb')

