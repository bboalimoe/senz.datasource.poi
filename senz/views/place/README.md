place module

##APIs

POST  /senz/places/    推测external用户places信息

Request parameters(in json):
external_user : (string) external数据点的用户标识
dev_key : (string) external开发者key
user_trace : (list) user的gps点集，

Response(Json form):
{"results":
    {"place_recognition":
        [{"estimateTime": 864600, "tag": "home", "ratio": 0.9905956112852664,
          "location": {"latitude": 39.9874398746627, "__type": "GeoPoint", "longitude": 116.43832351121905},
          "userId": "54f189d3e4b077bf8375477d"},
        {"estimateTime": 459000, "tag": "office", "ratio": 0.6235059760956175,
          "location": {"latitude": 39.98058323638342, "__type": "GeoPoint", "longitude": 116.30923811383433},
          "userId": "54f189d3e4b077bf8375477d"}]
     }
}


POST  /senz/places/internal/    senz内部推测用户places信息，从lifelogger取相应的user数据

Request parameters(in json):
user_id : (string) lifelogger中的user id

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


