#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wzf'

import subprocess
import socket
import logging

from monitor.common.openstack.threadgroup import ThreadGroup
from monitor.common.openstack import  timeutils

LOG = logging.getLogger(__name__)

'''Monitors for senz to observe system status

   Here just monitor whether system process is running or port is listening
'''

class BaseMonitor(object):
    def __init__(self, settings):
        self.tg = ThreadGroup()
        for ob, v in settings.items():
            self.tg.add_timer(v['interval'],
                              getattr(self, 'monitor_' + ob),
                              **v['args'])

    def monitor_process(self, key_word, handler):
        p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)

        lines = p3.stdout.readlines()
        if len(lines) > 0:
            return
        else:
            msg = "Process [%s] is lost at %s" % (key_word, timeutils.utcnow_ts())
            LOG.error(msg)
            if handler and handler.handle(msg):
                exit()

    def monitor_port(self, protocol, port, handler):
        address = ('127.0.0.1', port)
        socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
        client = socket.socket(socket.AF_INET, socket_type)

        try:
            client.bind(address)
        except Exception, e:
            pass
        else:
            msg = "port[%s-%s] is lost at %s" % (protocol, port, timeutils.utcnow_ts())
            LOG.error(msg)
            if handler and handler.handle(msg):
                exit()
        finally:
            client.close()

    def start(self):
        self.tg.wait()
