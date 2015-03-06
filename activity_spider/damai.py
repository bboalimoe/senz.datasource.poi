#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
'''
import StringIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
'''
from bidict import bidict
import json
import sys
sys.path.append("../utils")
import time
from senz.utils.util_opt import *
from senz.utils.geo_coding import GeoCoder
from senz.utils.avos_manager import *

class DamaiSpider(object):
        def __init__(self):
                self.filePath = "./damai/"
                self.mcid={'演唱会':1,'音乐会':2,'话剧歌剧':3,'舞蹈芭蕾':4,'曲苑杂坛':5,'体育比赛':6,'度假休闲':7}
                self.ccid={'流行':9,'摇滚':10,'民族':11,'音乐节':12,'其他演唱会':13,
                          '管弦乐':14, '独奏':15,'室内乐及古乐':16, '声乐及合唱':17, '其他音乐会':18,
                          '话剧 ':19,'歌剧 ':20,'歌舞剧 ':21,'音乐剧 ':22,'儿童剧 ':23,
                          '舞蹈 ':24,'芭蕾 ':25,'舞剧 ':26,
                          '相声 ':27,'魔术 ':28,'马戏 ':29,'杂技 ':30,'戏曲 ':31,'其他曲苑杂坛 ':32,
                          '球类运动':33,'搏击运动':34,'其它竞技':35,
                          '主题公园':36, '风景区':37, '展会':38, '特色体验':39, '温泉':40, '滑雪':41, '游览线路':42, '度假村':43, '代金券':44, '酒店住宿':45
                          }
                self.mcidDict=~bidict(self.mcid)
                self.ccidDict=~bidict(self.ccid)
                self.geoCodingDict = {}
                self.geoCodingDictFile = "./geoCodingDict.txt"
                #self.readGeoCodingDict(self.geoCodingDictFile)
                self.geoCoder = GeoCoder()
                self.avosClassName = "damai"
                self.avosManager = AvosManager()
                
        def readGeoCodingDict(self,filePath):
                with open(filePath) as fileInput:
                        self.geoCodingDict = json.loads(fileInput.read())

        def updateGeoCodingDict(self,filePath):
                with open(filePath,"w") as fileInput:
                        geoCodingDictJson = json.dumps(self.geoCodingDict,ensure_ascii=False)
                        fileInput.write(geoCodingDictJson)

        def crawl(self):
                outcomePathHead=self.filePath
                # get_source('http://www.damai.cn/projectlist.do?mcid=1&ccid=9')
                # print get_source('http://item.damai.cn/66780.html')
                ccidThresh={1:13,2:18,3:23,4:26,5:32,6:35,7:45}
                startMcid=3
                startCcid=21
                mcid=startMcid
                ccid=startCcid

                while mcid<=7:
                        mcidName=self.mcidDict[mcid]
                        while ccid<=ccidThresh[mcid]: #
                                print '当前数据存放地址：'
                                path=outcomePathHead+self.mcidDict[mcid]+'_'+self.ccidDict[ccid]+'.txt'
                                # path=outcomePathHead+'test.txt'
                                print path
                                uipath = unicode(path , "utf8")
                                #fileOut=open(uipath,'w')
                                pageIndex=1
                                while 1: # index of page keep changing until there is no perform list in the page
                                        #try:
                                                performListPage='http://www.damai.cn/projectlist.do?mcid=%s&ccid=%s&pageIndex=%s' % (mcid,ccid,pageIndex)
                                                print '当前页面目录：',performListPage
                                                listPage=get_source(performListPage)
                                                soup=BeautifulSoup(listPage)
                                                performList=soup.find(attrs={'id':'performList'})
                                                titleList=performList.find_all('h2')
                                                linkList=[]
                                                for each in titleList:
                                                        a=each.find('a')
                                                        linkList.append(a['href'])

                                                if len(titleList)== 0: # indicate the index of page has come to an end, ccid therefore needs to change
                                                        print 'this is an empty page'
                                                        break

                                                for eachshow in linkList:
                                                        timeInfo=[]
                                                        price=[]
                                                        print eachshow
                                                        showpage=get_source(eachshow)
                                                        # showpage=get_source('http://item.damai.cn/70686.html')
                                                        soup=BeautifulSoup(showpage,"html.parser")

                                                        try:
                                                                title=soup.find(attrs={'class':'title'}).get_text().strip().encode('utf-8') # get the title
                                                        except:
                                                                title='待定'
                                                        try:
                                                                location=soup.find(attrs={'itemprop':'location'}).get_text().strip().encode('utf-8') # get the location
                                                        except:
                                                                location='待定'
                                                        
                                                        #geocoding
                                                        lng = 0.0
                                                        lat = 0.0
                                                        if location in self.geoCodingDict:
                                                                lng,lat = self.geoCodingDict[location]
                                                        else:
                                                                locationList = location.split("-")
                                                                region = locationList[0].strip()
                                                                normRegion = region.replace(" ","").replace("（","").replace("）","").replace("(","").replace(")","")
                                                                if region in self.geoCodingDict:
                                                                        lng,lat = self.geoCodingDict[normRegion]
                                                                else:
                                                                        lng,lat = self.geoCoder.geoCoding(region)
                                                                        self.geoCodingDict[region] = (lng,lat)
                                                                        if lng==0.0 and lat==0.0 and len(locationList)>1:
                                                                                city = locationList[1].strip()
                                                                                if city in self.geoCodingDict:
                                                                                        lng,lat = self.geoCodingDict[city]
                                                                                else:
                                                                                        lng,lat = self.geoCoder.geoCoding(city)
                                                                                        self.geoCodingDict[city] = (lng,lat)
                                                                self.geoCodingDict[location] = (lng,lat)
                                                                
                                                        
                                                        
                                                        try:
                                                                pidList=[]
                                                                timeList=soup.find(attrs={'id':'perform'}).find_all('a') # get the time, which is a list
                                                                for index,eachtime in enumerate(timeList): # get the price for each time
                                                                        pid=eachtime['pid']
                                                                        currentPerformTime = eachtime['time'].encode('utf-8')
                                                                        timeInfo.append(currentPerformTime)
                                                                        
                                                                        # print eachtime['class'],type(eachtime['class'])
                                                                        if eachtime['class']==[u'grey']:
                                                                                price.append('暂无')
                                                                                continue
                                                                        
                                                                        if index>0:
                                                                                data={'type':'33',
                                                                                          'performID':pid,
                                                                                          'business':'1',
                                                                                          'IsBuyFlow':'False',
                                                                                          'sitestaus':'3'}
                                                                                post_data=urllib.urlencode(data)
                                                                                url='http://item.damai.cn/ajax.aspx?' + post_data
                                                                                newpage=get_source(url)
                                                                                soup=BeautifulSoup(newpage,"html.parser")
                                                                                priceLinkList=soup.find_all('a',attrs={'class':True,'price':True})

                                                                        else:
                                                                                priceLinkList=soup.find(attrs={'id':'price'}).find_all('a')
                                                                        priceList=[]
                                                                        for eachlink in priceLinkList:
                                                                                norlizedPrice=eachlink.get_text()
                                                                                norlizedPrice=norlizedPrice.replace(u'暂时无货，登记试试运气~',u' ( 无货 )').replace(u'点击进行预定登记',u' ( 可预定 )')
                                                                                priceList.append(norlizedPrice.encode('utf-8'))
                                                                        price.append(priceList)
                                                                        currentPerformPriceInfo = ",".join(priceList)
                                                                        #no end time
                                                                        date_time,start_time = getAvosTimeInfo(currentPerformTime)

                                                                        dataDict = {"name":title,"date":date_time,
                                                                        "start_time":start_time,"ticket":currentPerformPriceInfo,"region":location,"location":gps2GeoPoint(lat,lng),"category":TransferDict(mcidName)}
                                                                        try:
                                                                                self.avosManager.saveActivity(dataDict)
                                                                        except:
                                                                                print "avos exception!"
                                                                                continue
                                                        except:
                                                                print "show:%s, parse time and price error!" % eachshow
                                                                continue
                                                        '''
                                                        except:
                                                                timeInfo.append('待定')
                                                                price.append('待定')

                                                        mcidName=self.mcidDict[mcid]
                                                        ccidName=self.ccidDict[ccid]
                                                        titleName=title
                                                        placeName=location
                                                        data=[{"mcid": mcidName},
                                                                  {"ccid": ccidName},
                                                                  {"title": titleName},
                                                                  {"place": placeName},
                                                                  {"time": timeInfo},
                                                                  {"price": price}]
                                                        dataDict = {"mcid": mcidName,"ccid": ccidName,"title": titleName,"place": placeName,"time": time,"price": price}
                                                        normalizedData= json.dumps(data,ensure_ascii=False,sort_keys=True,indent=1)
                                                        normalizedData=normalizedData.replace('[\n {\n','{\n').replace('\n }\n]','\n}').replace('\n }, \n {\n',' ,\n')
                                                        #print normalizedData
                                                        fileOut.write(normalizedData+'\n\n\n')
                                                        fileOut.flush()

                                                        del timeInfo[:]
                                                        del price[:]
                                                                '''
                                        #except:
                                                print 'Error: something wrong'
                                                import sys
                                                info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1]) #todo log the exception info
                                                print info
                                                print sys.exc_info()
                                                pageIndex+=1 #change
                                ccid+=1
                        mcid+=1
                #self.updateGeoCodingDict(self.geoCodingDictFile)

def TransferDict(CateName):

    dataDict = {
    "演唱会":"音乐",
    "音乐会":"音乐",
    "话剧歌剧":"戏剧",
    "舞蹈芭蕾":"音乐",
    "曲苑杂坛":"戏剧",
    "体育比赛":"运动",
    "度假休闲":"旅行",
    "儿童亲子":"其他",
    }
    return dataDict[CateName]


if __name__ == "__main__":
        spider = DamaiSpider()
        spider.crawl()
