__author__ = 'wzf'


import settings
import os

def findGroup(avosClassName):
    #find leancloud project of avosClassName
    if avosClassName:
        for groupName in settings.groups:
            if avosClassName in settings.groups[groupName]['avos_app_classes_list']:
                return groupName

    return 'base'

def getAppSettings(avosClassName):
    group = findGroup(avosClassName)
    return settings.groups[group]


if __name__ == '__main__':
    print os.getcwd() + os.path.sep + 'logs'
    getAppSettings("")
    getAppSettings("LocationRecognition")