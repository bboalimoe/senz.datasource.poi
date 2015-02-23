# Location module

## 用法

    import location
    location.cluster(jsonArray)
    
## 示例

见`test.py`
    
## 接口及参数列表

    def cluster(jsonArray, maxClusterRadius=0.00125, samplingInteval=10000, minValidClusterSize=30,
                       timeRanges=defaultTimeRanges, tagOfTimeRanges=defaultTagOfTimeRanges):

1. jsonArray: 数据源。格式示例见`testLocation.json`
 
2. maxClusterRadius: 地点范围半径的最大值。默认为0.00125。

3. samplingInteval: 时间采样频率，单位为ms。默认为10000，即 10s 采一个样。

4. timeRanges: 时间范围。格式为:  `[[22, 23, 0, 1, 2, 3, 4, 5, 6, 7], [9, 10, 11, 14, 15, 16, 17]]` 每个数组表示某种情景的时间范围，元素的值为`hour`。

5. tagOfTimeRanges: tag列表。格式为: `["home", "office"]`。顺序应该与`timeRanges`保持一致。

6. tagThreshold: 给地点加tag的阈值。默认为30，即聚类内有30个数据点在tag对应的时间段内，即给地点加上这个tag。