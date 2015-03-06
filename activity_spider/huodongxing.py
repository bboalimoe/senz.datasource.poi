#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
sys.path.append("../utils")
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
import time
from senz.utils.util_opt import *
from senz.utils.geo_coding import GeoCoder
from senz.utils.avos_manager import *
import re

class HuodongxingSpider(object):
        """
        Deprecated!

        """
	def __init__(self):
		self.categoryList=["沙龙","创业","互联网","公益","课程","聚会","论坛","北京","休闲","免费","文艺","TEDx","校园","培训","交友"]
		#self.cityList = ["beijing","shanghai","guangzhou"]
		self.timeType = "t1";
		#self.geoCodingDictFile = "./geoCodingDict.txt"
		#self.geoCodingDict = {}
		#self.readGeoCodingDict(self.geoCodingDictFile)
		self.geoCoder = GeoCoder()
		self.avosClassName = "huodongxing"
		self.avosManager = AvosManager()
		self.baseUrl = "http://www.huodongxing.com"
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
		for categoryCn in self.categoryList:
			categoryUrl = "http://www.huodongxing.com/events?type=0&show=list&d=%s&tag=%s" % (self.timeType,categoryCn)
			nextPageUrl = categoryUrl
			
			currentPageNum = 1
			while nextPageUrl != "":
				eventUrlList = []
				print nextPageUrl.decode("utf8").encode("gbk")
				listPage=get_source(nextPageUrl)

				soup=BeautifulSoup(listPage)
				allEventsInfo=soup.find(attrs={'class':'event-horizontal-list'}).find_all("li")
                #todo huodongxing网页规则出问题了！

				for eventInfo in allEventsInfo:
					try:
						eventUrl = self.baseUrl + eventInfo.find_all("a")[0]["href"]
						eventUrlList.append(eventUrl)
					except:
						continue
				
				
				nextPageNum = 1;
				try:
					paginationList = soup.find(attrs={'class':'pagination'}).find_all("li")
					for paginationInfo in paginationList:
						if paginationInfo["class"][0] != "last-child":
							continue
						else:
							onclickInfo = paginationInfo.find_all("a")[0]["onclick"]
							start_tmp = onclickInfo.find("(")
							end_tmp = onclickInfo.find(")")
							nextPageNum = int(onclickInfo[start_tmp+2:end_tmp-1])
							break
					
					if nextPageNum > currentPageNum:
						nextPageUrl = categoryUrl + "&page=%s" % nextPageNum
						currentPageNum = nextPageNum
					else:
						nextPageUrl = ""
				except:
					nextPageUrl = ""
				print "event num:%s" % len(eventUrlList)
				for eventUrl in eventUrlList:
					eventPage=get_source(eventUrl)
					soup=BeautifulSoup(eventPage)
					media_body = soup.find(attrs={'class':'media-body'})
					eventTitle = media_body.find(attrs={'class':'media-heading'}).get_text().strip().encode('utf-8')
					mediaBodyDivList = media_body.find_all("div")
					mediaInfoDict = {"icon-time":"","icon-place":""}
					for mediaBodyDiv in mediaBodyDivList:
						try:
							mediaClass = mediaBodyDiv.find_all("em")[0]["class"][0]
							if mediaClass in mediaInfoDict.keys():
								mediaInfoDict[mediaClass] = mediaBodyDiv.get_text().strip().encode('utf-8')
						except:
							continue
					try:
						mediaInfoDict["icon-time"] = mediaInfoDict["icon-time"].replace("年","-").replace("月","-").replace("日","")
						icon_timeList = mediaInfoDict["icon-time"].split(" ～ ")
						
						start_str = icon_timeList[0]
						if start_str.count(":") == 1:
							start_str += ":00"
						if len(icon_timeList) > 1:
							end_str = icon_timeList[1]
						if end_str.count(":") == 1:
							end_str += ":00"

						date_time,start_time,end_time = getAvosTimeInfo(start_str, end_str)
						
						eventLocation = mediaInfoDict["icon-place"]
						left_str = "（";
						right_str = "）"
						region = eventLocation.replace(" ","").replace(left_str,"").replace(right_str,"").replace("(","").replace(")","")
						longitude,latitude = self.geoCoder.geoCoding(region)
					except:
						continue

					dataDict = {"name":eventTitle,"date":date_time,
					"start_time":start_time,"end_time":end_time,"ticket":"","region":eventLocation,"location":gps2GeoPoint(latitude,longitude),"category":categoryCn}
					try:
						self.avosManager.saveActivity(dataDict)
					except:
						print dataDict
						print "avos exception! eventUrl:%s" % eventUrl
						continue
						

		#self.updateGeoCodingDict(self.geoCodingDictFile)

if __name__ == "__main__":
	spider = HuodongxingSpider()
	spider.crawl()
