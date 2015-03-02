#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import *
import sys
import json
import sys
import datetime
sys.path.append("../utils")
from senz.utils.avos_manager import *
for i in sys.path:
    print i
#print "sys.path   ",sys.path

def distance(lon1, lat1, lon2, lat2):
        """
        calulate distence from GPS
        :param lon1:
        :param lat1:
        :param lon2:
        :param lat2:
        :return:
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return 6371300 * c

def iso2timestamp(iso_time): #avos date type {u'__type': u'Date', u'iso': u'2015-05-23T11:15:00.000Z'}
        t = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.000Z")
        return long(time.mktime(t))

def ISOString2Time( s ):
    '''
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123
    把一个时间转化为秒
    '''
    d=datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())

def Time2ISOString( s ):
    '''
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(s) ) )


class UserActivityMapping(object):

        #todo  1.update the db mapping results periodically
        #todo  2.retrieve the specific user's mapping results from the db
        #todo  3.outdated info is not counted in the afterwards calculation

        #todo  4.Naive Bayes added

        def __init__(self):
                self.avosManager = AvosManager()
                self.mappingList = {}
                self.users = {}
                self.activities = []

                #todo
                self.mapped = False # tell the method if updating the results
                #todo
                self.lastMappingTime = None  # retrieve the time from the db or the file
                                             # it's for checking the mapping period in case the info is outdated

        #Consider whether user in this activity
        def __isInActivity(self,user,activity):


                aLon=activity['location']['longitude']
                aLat=activity['location']['latitude']
                activeTimes = []
                for oneTime in user:
                        uLon=oneTime['longitude']
                        uLat=oneTime['latitude']
                        if(distance(aLon, aLat, uLon, uLat)<100):
                                activeTimes.append(oneTime['timestamp'])
                print "start time", activity['start_time']
                if len(activeTimes) == 0:
                        return 0
                #print "start time", activity['start_time']
                startTime = iso2timestamp(activity['start_time']['iso'])               
                endTime = iso2timestamp(activity['end_time']['iso']) if 'end_time' in activity else long(sys.maxint)*1000

                actives = len([timestamp for timestamp in activeTimes if timestamp>=startTime and timestamp<=endTime])
                if actives >= len(activeTimes)*0.5:
                        return 1
                else:
                        return 0

        def __isMatchTimeLoc(self):
            """
            deprecated
            :return:
            """
            return
                        
        
        def __getUserList(self):
                """
                the location_record's userId(deviceid)
                :return:
                """
                print 'Getting user list ...'
                L = 200
                start = 0
                res_len = L
                while res_len == L:                       
                        res = json.loads(self.avosManager.getData('location_record',limit=L, skip=start))['results']
                        res_len = len(res)
                        for user in res:
                                if user['userId'] not in self.users:
                                        self.users[user['userId']]=[user]
                                else:
                                        self.users[user['userId']].append(user);
                        start = start+L
                print 'Done'

        def __getUserLastLocations(self,userId):

                print "get user %s activities...".format(userId)
                L = 200
                start = 0
                res_len = L
                while res_len == L:
                        res = json.loads(self.avosManager.getData('activities' ,limit=L, skip=start))['results']
                        res_len = len(res)
                        self.activities = self.activities+res
                        start = start+L
                print 'Done'

        def _getLastPossibleActivities(self): #first return the last 3 days(3*24*60*60 sec)'s activities before the timeNow

                print 'Getting activities ...'
                L = 200
                start = 0
                res_len = L
                while res_len == L:
                    res = json.loads(self.avosManager.getData('activities' ,limit=L, skip=start, where={"start_time":{"$gte":{u'__type': u'Date', u'iso': time.strftime('%Y-%m-%d %H:%M:%S')} }}))['results']
                    res_len = len(res)
                    self.activities = self.activities+res
                    start = start+L
                print 'Done'


        def __getActivities(self):
                print 'Getting activities ...'
                L = 200
                start = 0
                res_len = L
                while res_len == L:                       
                        res = json.loads(self.avosManager.getData('activities' ,limit=L, skip=start))['results']
                        res_len = len(res)
                        self.activities = self.activities+res
                        start = start+L
                print 'Done'
                
        def mapping(self, saveTo=0 ):

                #todo saveTo indicates where to save the data
                ## 0 -> db
                ## 1->  local file
                ## ...
                """
                calculate every user's mapping results
                :return:
                """
                self.__getUserList()
                self.__getActivities()

                for userId,user in self.users.items():
                        print 'Mapping user: id=  '+userId+' ...'
                        self.mappingList[userId] = []
                        for activity in self.activities:
                            #print "activity", activity['objectId']
                            print "fuck\n\n\n\n\n\n"
                            if self.__isInActivity(user,activity):
                                    #print "activity['objectId']",activity['objectId']
                                    self.mappingList[userId].append(activity['objectId'])
                        print 'Done'
                        self.avosManager.saveData("MappingResults",{"userid":userId,"activities":self.mappingList[userId]})
                #todo only map one day's user location&activity data  and save one day's matching data into avos


                print 'Mapping finished!'


        def mappingActivitiesByUser(self,userId, amount):
            """
            Logic: this will be triggered after Big events happened like Jay chou or Beyonce live!

            search the activities by the user
            :param userId: the unique id that stored in db，it maps the mac one on one
            :return: the list of last ten activities that the user has attended
            """

            """
            self.mapping()
            #print "mappinglist", self.mappingList
            activityIdList = self.mappingList[userId] #mapping list is usr's activitys' objectid
            print activityIdList

            if amount < 0: #all
                return activityIdList
            else:
                if len(activityIdList) > amount: # amount
                    return activityIdList[:amount]
                else: # all
                    return activityIdList
            """
            results = self.avosManager.getData("MappingResults",where={"userid":userId})
            results = json.loads(results)
            print results["results"][0]
            return results


        def dump2file(self,filename='./mapping_results'):
            """
            dump the info to the file in the harddisk
            :param filename:
            :return:
            """


            print 'Dumping result to file: '+filename+' ...'
            f = open(filename,'w')
            f.write('No UserId       \tActivities\n');
            n=1
            for user,activities in self.mappingList.items():
                    line = unicode.encode(user,'utf8')+'\t'
                    for activity in activities:
                            line = line+unicode.encode(activity,'utf8')+'/'
                    line = line[:-1]+'\n\n\n\n'
                    f.write(str(n)+'  '+line);
                    n=n+1
            f.close()
            print 'Dumping finished!'

        def dump2db(self,GPSlist,userId):
            """
            dump the info to db
            :return:
            """

            for gps in GPSlist:
                result = self.avosManager.saveData("UserLocationTrace",{"latitude":gps['latitude'],"longitude":gps["longitude"],"activityId":"",
                                                               "timpstamp":gps['timestamp'],"userId":userId})
                if not result:
                   print "save error: userid:%s".format(userId)




if __name__=="__main__":
        #mapping = UserActivityMapping()

        #mapping.mapping()
        #mapping.dump2file('./mapping_result.txt')


        print "timenow ", time.strftime('%Y-%m-%d %H:%M:%S')
        print "timestamp", Time2ISOString(iso2timestamp("2011-08-20T02:06:57.000Z"))
        print ISOString2Time(time.strftime("%Y-%m-%d %H:%M:%S"))
        import time
        print time.time()  #unix epoch time 和 timestamp一致，存入avos后台的utc也是iso和前面是一个转化值。所以呈现出来的string形式，与北京时间不同，差8小时。
        Map = UserActivityMapping()
        res = json.loads(Map.avosManager.getDateGreatData("activities",time.strftime("%Y-%m-%d %H:%M:%S") ))['results']

        print "length", len(res)
        for i in res:
            print "timenow ",i
        Map.mapping()


        where={"start_time":{"$gte":{"__type": "Date", "iso": time.strftime("%Y-%m-%d %H:%M:%S") } }}

        where={"createdAt":{"$gte":{"__type":"Date","iso":"2011-08-21T18:02:52.249Z"}}}
        print Map.mappingActivitiesByUser("e19e3c6313556d4c",5)["results"][0]


        {u'__type': u'Date', u'iso': u'2015-05-23T11:15:00.000Z'}