__author__ = 'wuzhifan'

import sys
import os
import logging


sys.path.append(os.path.dirname(os.getcwd()))
from SenzPoi.monitor.monitors import BaseMonitor
from SenzPoi.monitor import settings

def config():
    FILE = os.getcwd()
    logging.basicConfig(filename=os.path.join(FILE,'log.txt'),level=logging.INFO)

def main():
    config()
    monitor = BaseMonitor(settings.MONITORS)
    monitor.start()

if __name__ == '__main__':
    main()