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

def get_task(task_name):
    for e in settings.functions:
        if settings.functions[e]['type'] == 'collection':
            get_task(settings.functions[e])
        if settings.functions[e]['type'] == 'task' and e == task_name:
            return settings.functions[e]

if __name__ == '__main__':
    print os.getcwd() + os.path.sep + 'logs'
    getAppSettings("")
    getAppSettings("LocationRecognition")