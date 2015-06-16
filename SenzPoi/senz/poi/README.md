# poi module

    poi 操作模块。通过百度api，iBeacon，geo fence等方法获取poi信息，并可由用户定义poi group。

##用法
    #百度api获取poi
    from senz.poi import poi

    poiGetter = poi.PoiGet()
    poi = poiGetter.getPoi()

    #用户自定义poi group CRUD
    from senz.poi import poiGenerator

    poiGen = poiGenerator.PoiGenerator()
    #添加
    poiGen.addPoiGroupByName(name, username)
    poiGen.addPoiGroup(name, userId)
    #获取
    poiGen.getPoiGroupIdByName(poiGroupName, username)
    poiGen.getPoiGroupByGps(user, lat, lng)
    poiGen.getPoiGroups(username)
    #更新
    poiGen.updatePoiGroupMemberByName(poiGroupName, username, lat, lng)
    #删除
    poiGen.deletePoiGroupByName(poiGroupName, username)


## 示例

    见`test.py`