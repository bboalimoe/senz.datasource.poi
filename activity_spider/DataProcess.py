__name__ = "bboalimoe"

#todo collect the data from the tables ..damai, huodongxing, douban
#todo activity clustered based on the category of douban

from activity_spider.damai import DamaiSpider
from activity_spider.douban import DoubanSpider
#from huodongxing import HuodongxingSpider

class DataProcess(object):

     def __init__(self):
            self.damai  = DamaiSpider()
            self.douban = DoubanSpider()
            #self.hdxing = HuodongxingSpider()

     def parseAndReassign(self):

         """
         parse the activity's type and Assign to specific type group based on the douban classification
         :return:
         """""

     def uploadData(self):

         """
         upload the Data to one Table
         :return:
         """
