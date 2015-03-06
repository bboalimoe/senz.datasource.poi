# -*- encoding:utf-8 -*-

from threading import Thread
import sys

from activity_spider.damai import DamaiSpider
from douban import DoubanSpider


sys.path.append("../utils")
from senz.utils.timer import SchedTimer

def multi_thread_crawl():


    damai = Thread(target=DamaiSpider().crawl)
    douban = Thread(target=DoubanSpider().crawl)
    #todo huodongxing website changed
    #huodongxing = Thread(target=HuodongxingSpider().crawl)
    #crawling with multi-threads

    #todo  1 data from the crawler must be update everyday.
    #todo  2 new data different from the old ones in the table are inserted into the db,others are not
    #todo  3 old data are kept forever for 2 reasons:   1.mapping action will create pointer to the data kept before  2.this backup is the unique one in the system db.
    damai.start()
    douban.start()
    #huodongxing.start()



    #damai.join()
    #douban.join()
    #todo in case it runs toooo long, we set it in asynchronous way, so we can response in time
    #huodongxing.join()
    print 'Spider Stops'

    return


def runCrawler(): #todo trigger the Crawler in diffrent strategy


    print '爬虫将在24点运行...'
    t = SchedTimer(24,00,00)
    t.start(multi_thread_crawl)

if __name__=="__main__":

    #runCrawler()
    multi_thread_crawl()