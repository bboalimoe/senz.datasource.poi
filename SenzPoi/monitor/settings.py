__author__ = 'wuzhifan'

from monitor.common.handlers import *


#Configures of created monitors
MONITORS = {
    'port': {
        'interval': 5,
        'args': {
            'protocol': 'tcp',
            'port': 8099,
            'handler': EmailHandler(),
            'initial_delay' : 60,
        }
    },
    #'process' : {
    #    'interval' : 10,
    #    'args' : {
    #        'key_word' : 'senz'
    #        'handler' : EmailHandler(),
    #        'initial_delay' : None,
    #    }
    #}
}

