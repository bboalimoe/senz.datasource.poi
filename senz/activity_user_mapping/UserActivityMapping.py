#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import *
import sys
import json
import sys
sys.path.append("../utils")
from avos_manager import *
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

def iso2timestamp(iso_time):
        t = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.000Z")
        return long(time.mktime(t)*1000)

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

                if len(activeTimes) == 0:
                        return 0
                
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
                                if self.__isInActivity(user,activity):
                                        self.mappingList[userId].append(activity['objectId'])
                        print 'Done'
                print 'Mapping finished!'


        def mappingActivitiesByUser(self,userId, amount):
            """
            Logic: this will be triggered after Big events happened like Jay chou or Beyonce live!

            search the activities by the user
            :param userId: the unique id that stored in db，it maps the mac one on one
            :return: the list of last ten activities that the user has attended
            """


            self.mapping()
            activityList = self.mappingList[userId]
            if amount < 0: #all
                return activityList
            else:
                if len(activityList) > amount: # amount
                    return activityList[:amount]
                else: # all
                    return activityList


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

        def dump2db(self):
            """
            dump the info to db
            :return:
            """
            pass
            #todo dump the mapping results to the db



if __name__=="__main__":
        #mapping = UserActivityMapping()

        #mapping.mapping()
        #mapping.dump2file('./mapping_result.txt')
        Map = UserActivityMapping()
        print Map.mappingActivitiesByUser("2b4e710aab89f6c5")
