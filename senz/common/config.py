__author__ = 'wzf'

def findGroup(self, avosClassName):
    #find leancloud project of avosClassName
    if avosClassName:
        for groupName in settings.groups:
            if avosClassName in settings.groups[groupName]['avos_classes_list']:
                return groupName

    return 'base'