# -*- encoding=utf-8 -*-
# __author__ = 'Zhong.zy'

#sys.path.append('..')

from senz.common.avos.avos_manager import *
from senz.common.utils.util_opt import *


class PoiGenerator(object):
    #exception will be caught in the view level
    def __init__(self):
        self.avos = AvosManager()

    def inQueryDict(self, className, **kwargs):
        cond = {'where': kwargs, 'className': className}
        query = {'$inQuery': cond}
        return query

    def addPoiGroupByName(self, name, username):
        userId = self.avos.getUserIdByName(username)
        self.addPoiGroup(name, userId)

    def addPoiGroup(self, name, userId):
        user = dict(__type='Pointer', className='_User', objectId=userId)
        dataDict = dict(name=name, owner=user)
        self.avos.saveData('PoiGroup', dataDict)

    def getPoiGroupIdByName(self, poiGroupName, username):
        user = dict(__type='Pointer', className='_User',
                    objectId=self.avos.getUserIdByName(username))
        return self.avos.getIdByCondition('PoiGroup', name=poiGroupName, owner=user)

    def getPoiGroupByGps(self, user, lat, lng):

        inQuery = self.inQueryDict('PoiGroup', owner=self.inQueryDict('_User', username=user))
        cond = dict(location=gps2GeoPoint(lat, lng), poiGroup=inQuery)
        res = self.avos.getData('PoiGroupMember', keys='poiGroup.name', include='poiGroup', where=json.dumps(cond))
        poiGroups = [(poiGroup['poiGroup']['name']).encode('utf-8') for poiGroup in json.loads(res)['results']]
        poiGroups = [i.replace("'", "\"") for i in poiGroups]
        return poiGroups

    def getPoiGroups(self,username):
        # get poi groups!
        user = dict(__type="Pointer", className="_User",
                    objectId=self.avos.getUserIdByName(username))

        return self.avos.getData("PoiGroup",where={"owner":user})


    def addPoiGroupMemberByName(self, poiGroupName, username, lat, lng):

        poiGroupId = self.getPoiGroupIdByName(poiGroupName, username)
        if poiGroupId != None:
            return self.addPoiGroupMember(poiGroupId, lat, lng)

        else:
            print username + " has no PoiGroup called '" + poiGroupName + "'"
            return None

    def updatePoiGroupMemberByName(self, poiGroupName, username, lat, lng):


        results = self.deletePoiGroupMemberByName(poiGroupName, username, lat, lng)
        if not results:
            return None

        results = self.addPoiGroupMemberByName(poiGroupName, username, lat, lng) # {"error":"something"}

        return results


    def addPoiGroupMember(self, poiGroupId, lat, lng):

        group = dict(__type='Pointer', className='PoiGroup', objectId=poiGroupId)
        dataDict = dict(poiGroup=group, location=gps2GeoPoint(lat, lng))

        return self.avos.saveData('PoiGroupMember', dataDict)

    def getPoiGroupMembersByName(self, poiGroupName, username):

        poiGroupId = self.getPoiGroupIdByName(poiGroupName, username)
        if poiGroupId == None:
            print username + " has no PoiGroup called '" + poiGroupName + "'"
        else:
            cond = dict(poiGroup=dict(__type='Pointer', className='PoiGroup', objectId=poiGroupId))
            res = self.avos.getData('PoiGroupMember', where=json.dumps(cond))
            memberList = json.loads(res)['results']
            return [(member['place']['latitude'], member['place']['longitude']) for member in memberList]

    def deletePoiGroupMemberByName(self, poiGroupName, username, lat, lng):
        poiGroupId = self.getPoiGroupIdByName(poiGroupName, username)
        group = dict(__type='Pointer', className='PoiGroup', objectId=poiGroupId)
        objId = self.avos.getIdByCondition('PoiGroupMember', poiGroup=group, location=gps2GeoPoint(lat, lng))
        self.avos.deleteData('PoiGroupMember', str(objId))

    def deletePoiGroupByName(self, poiGroupName, username):
        poiGroupId = self.getPoiGroupIdByName(poiGroupName, username)
        if poiGroupId == None:

            a = username + " has no PoiGroup called '" + poiGroupName + "'"
            return {"error": a}
        else:
            cond = dict(poiGroup=dict(__type='Pointer', className='PoiGroup', objectId=poiGroupId))
            res = self.avos.getData('PoiGroupMember', keys='objectId', where=json.dumps(cond))
            memberList = json.loads(res)['results']
            for member in memberList:
                self.avos.deleteData('PoiGroupMember', str(member['objectId']))
            return self.avos.deleteData('PoiGroup', str(poiGroupId))


if __name__ == '__main__':
    poi = PoiGenerator()
    #poi.addPoiGroupByName('公园','zhong1')
    #for i in range(1,6):
    #        poi.addPoiGroupMemberByName('公园','zhong1',11+i,113)
    #poi.deletePoiGroupMemberByName('跑步','zhong2',13,113)
    #poi.deletePoiGroupByName('跑步','zhong1')
    #print poi.getPoiGroupMembersByName('跑步','zhong1')
    print poi.getPoiGroups("zhong2")
    #print poi.getPoiGroupByGps('zhong1', 16, 113)

