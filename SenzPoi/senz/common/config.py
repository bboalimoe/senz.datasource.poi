__author__ = 'wzf'

from SenzPoi.senz.common import settings


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

def get_task(task_name, tasks=settings.tasks):
    for e in tasks:
        #print e
        if tasks[e]['type'] == 'collection':
            if 'tasks' not in tasks[e]:
                continue
            in_collection = get_task(task_name, tasks[e]['tasks'])
            if in_collection:
                return in_collection
        if tasks[e]['type'] == 'task' and e == task_name:
            return tasks[e]

if __name__ == '__main__':
    #print os.getcwd() + os.path.sep + 'logs'
    #getAppSettings("")
    #getAppSettings("LocationRecognition")

    print get_task('parse_poi')