# Location module

## 用法

    import location
    location.cluster(jsonArray)
    
## 示例

见`test.py`
    
## 接口及参数列表

### 情景识别接口

    def cluster(jsonArray, maxClusterRadius=0.00125, samplingInteval=10000,
                       timeRanges=defaultTimeRanges, tagOfTimeRanges=defaultTagOfTimeRanges, timeThreshold = 300000,
                       ratioThreshold = 0.4)

### 参数列表

1. jsonArray: 数据源。格式示例见`testLocation.json`
 
2. maxClusterRadius: 地点范围半径的最大值。默认为0.00125。

3. samplingInteval: 时间采样频率，单位为ms。默认为10000，即 10s 采一个样。

4. timeRanges: 时间范围。格式为:  `[[22, 23, 0, 1, 2, 3, 4, 5, 6, 7], [9, 10, 11, 14, 15, 16, 17]]` 每个数组表示某种情景的时间范围，元素的值为`hour`。

5. tagOfTimeRanges: tag列表。格式为: `["home", "office"]`。顺序应该与`timeRanges`保持一致。

6. timeThreshold: 给地点加tag的时间阈值，用于剪枝。默认为300000，即停留时间为300000 ms（5 min）以下的地点直接忽略。

7. ratioThreshold: 给地点加tag的比率阈值。默认为 0.4。对于某情景，某类簇的数据占所有数据的比率如高于这个值则加上情景tag，否则不加。

### 返回值格式

返回值示例：

    [{"estimateTime": 2810000, "tags": [{"estimateTime": 2420000, "ratio": 0.8962962962962963, "tag": "home"}], "longitude": 116.34378083770036, "latitude": 39.89735272632654}]

返回值为一个数组。数组的每个元素的属性如下：

1. longitude : 经度

2. latitude : 纬度

3. estimateTime : 在该地点停留时间的估计值。由于经过采样后还原，可能与原始数据略有误差。保证大于`timeThreshold`。

4. tags : tag 列表，每个 tag 代表一个情景。tag 的格式如下：

tag示例：

    [{"estimateTime": 2420000, "ratio": 0.8962962962962963, "tag": "home"}] 

1. tag : tag 名称，与入参`tagOfTimeRanges`相符。

2. estimateTime : 该地点在该情景下停留时间的估计值。由于经过采样后还原，可能与原始数据略有误差。

3. ratio : 该情景下该地点数据占全体数据的比例。保证大于`ratioThreshold`。

所有属性为必有。