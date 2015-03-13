###senz poi service

1, 对用户位置数据进行分析，推测用户行为；

2, 生成并记录POI信息，并提供POI相关的定制化操作和接口。


###主要功能

###Location  Recognition

###rest api调用

   http://server_url/senz/usr_loc_tag/

###User Activity Mapping

###rest api调用

   http://server_url/senz/initiate_map/   #mapping活动
   http://server_url/senz/activity/       #获取活动

###poi

###rest api调用

   http://server_url/senz/poi_Gpeacon/
   http://server_url/senz/baidu_poitype/  #使用百度pai获取poi

   http://server_url/senz/poi/    #获取距给定点最近的五个用户定义poi group
   http://server_url/senz/poi_groups/   #用户创建/删除poi group
   http://server_url/senz/poi_group/   #获取用户定义的所有poi group
   http://server_url/senz/poi_group_member/   #添加/修改/删除poi group的成员

###系统模块

###Log

   日志信息存放在senz_project_path/logs/senz.log

###用法

   import logging

   LOG = logging.getLogger(__name__)

   LOG.debug("this is an debug log")
   LOG.info("this is an info log")
   LOG.warning("this is an warning log")
   LOG.error("this is an error log")
   LOG.critical("this is an critical log")

