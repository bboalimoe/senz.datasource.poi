POST  /senz/activities/    根据用户行迹推测是否参加了activity

Request parameters(in json):
user_trace : (list) user的gps点集
last_days : (int) 表示需要推测的从现在开始的时间窗口

Response(Json form):
{"results":
    {"internal_place_recognition":
        [{"estimateTime": 864600, "tag": "home", "ratio": 0.9905956112852664,
          "location": {"latitude": 39.9874398746627, "__type": "GeoPoint", "longitude": 116.43832351121905},
          "userId": "54f189d3e4b077bf8375477d"},
        {"estimateTime": 459000, "tag": "office", "ratio": 0.6235059760956175,
          "location": {"latitude": 39.98058323638342, "__type": "GeoPoint", "longitude": 116.30923811383433},
          "userId": "54f189d3e4b077bf8375477d"}]
     }
}
