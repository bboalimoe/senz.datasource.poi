place module

##APIs

POST  /senz/places/    推测用户places信息

Request parameters:
user_id : (string) lifelogger数据库中UserLocation的user
sampling_interval : (int)  trace数据点的采样时间，单位：s
time_threshold : （int） 用于筛选place类别，place中停留时间小于time_threshold的类别会被过滤掉，单位：s

Response(Json form):
{"results":
    [{"tag": "office", "ratio": 0.6387225548902196, "latitude": 39.98086796425048, "estimateTime": 405600,
      "userId": "54f189d3e4b077bf8375477d", "longitude": 116.30966020278602},
    {"tag": "home", "ratio": 0.99822695035461, "latitude": 39.987488291767875, "estimateTime": 576600,
      "userId": "54f189d3e4b077bf8375477d", "longitude": 116.43829548872655}]
}
