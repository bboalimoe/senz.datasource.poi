#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../utils")
from bs4 import BeautifulSoup
'''
import StringIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
'''
from senz.common.utils.geo_coding import GeoCoder
from senz.common.avos.avos_manager import *

class DoubanSpider(object):
	def __init__(self):
		self.categoryDict={'音乐':'music','戏剧':"drama",'讲座':"salon",'聚会':"party",'电影':"film",'展览':"exhibition",'运动':"sports",'公益':"commonweal",'旅行':"travel","其他":"others"}
		self.cityList = ["beijing","shanghai","guangzhou"]
		self.timeType = "week";
		#self.geoCodingDictFile = "./geoCodingDict.txt"
		#self.geoCodingDict = {}
		#self.readGeoCodingDict(self.geoCodingDictFile)
		self.geoCoder = GeoCoder()
		self.avosClassName = "douban"
		self.avosManager = AvosManager()
	'''
	def readGeoCodingDict(self,filePath):
		with open(filePath) as fileInput:
			self.geoCodingDict = json.loads(fileInput.read())

	def updateGeoCodingDict(self,filePath):
		with open(filePath,"w") as fileInput:
			geoCodingDictJson = json.dumps(self.geoCodingDict,ensure_ascii=False)
			fileInput.write(geoCodingDictJson)
	'''
	def crawl(self):
		for city in self.cityList:
			for categoryCn,categoryEn in self.categoryDict.iteritems():
				categoryUrl = "http://%s.douban.com/events/%s-%s" % (city,self.timeType,categoryEn)
				nextPageUrl = categoryUrl

				while nextPageUrl != "":
					print nextPageUrl
					listPage=get_source(nextPageUrl)

					soup=BeautifulSoup(listPage)
					allEventsInfo=soup.find(attrs={'class':'events-list events-list-pic100 events-list-psmall'}).find_all("li")

					for eventInfo in allEventsInfo:
						try:
							eventTitle = eventInfo.find(attrs={'class':'title'}).get_text().strip().encode('utf-8')
							eventTimeInfoList = eventInfo.find(attrs={'class':'event-time'}).find_all("time")
							eventTimeDict = {"startDate":"","endDate":""}
							for eventTimeInfo in eventTimeInfoList:
								itemprop = eventTimeInfo["itemprop"]
								DateTimeInfo = eventTimeInfo["datetime"]
								if itemprop not in eventTimeDict.keys():
									continue
								eventTimeDict[itemprop] = DateTimeInfo.replace("T"," ")
							eventLocation = eventInfo.find(attrs={'itemprop':'location'}).get("content","")
						except:
							continue
						try:
							longitude = float(eventInfo.find(attrs={'itemprop':'longitude'}).get("content",""))
							latitude = float(eventInfo.find(attrs={'itemprop':'latitude'}).get("content",""))
						except:
							longitude,latitude = lng,lat = self.geoCoder.geoCoding(eventLocation)
						ticketFee = eventInfo.find(attrs={'class':'fee'}).get_text().strip().encode('utf-8')
						
						date_time, start_time, end_time = getAvosTimeInfo(eventTimeDict["startDate"], eventTimeDict["endDate"])
                        #todo change the category,but now we use the douban category as a standard
						dataDict = {"name":eventTitle,"date":date_time,
						"start_time":start_time,"end_time":end_time,"ticket":ticketFee,
                        "region":eventLocation,
                        "location":gps2GeoPoint(latitude,longitude),
                        "category":categoryCn,
                        "source" : DoubanSpider.__name__}

						try:
							self.avosManager.saveActivity(dataDict)
						except:
							print "avos exception!"
							continue
							
							
					
					
					#nextpage
					nextInfo = soup.find(attrs={'rel':"next"})
					if nextInfo!= None:
						next = nextInfo.get("href","")
					else:
						next = ""
					if next != "":
						nextPageUrl = categoryUrl + next
					else:
						nextPageUrl = ""

		#self.updateGeoCodingDict(self.geoCodingDictFile)

if __name__ == "__main__":
	spider = DoubanSpider()
	spider.crawl()
