# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import logging

import smtplib
import email

LOG = logging.getLogger(__name__)

# handlers for monitor events

EMAIL_HOST = 'smtp.163.com'
EMAIL_USER = 'senz_notify'
EMAIL_PWD  = 'lovesenz'
EMAIL_POSTFIX = '163.com'
TO_EMAIL = 'senz_notify@163.com'


class EmailHandler(object):
    def __init__(self):
        pass

    def handle(self, message):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(EMAIL_HOST)
            smtp.login(EMAIL_USER, EMAIL_PWD)
            smtp.sendmail(EMAIL_USER+"@"+EMAIL_POSTFIX, TO_EMAIL, message)
            smtp.quit()
        except Exception ,s:
            s = str(s)
            s = s.encode('gbk')
            print s
            print 'email send failed.'

if __name__ == '__main__':
    ob = EmailHandler()
    ob.handle("test email sendor")