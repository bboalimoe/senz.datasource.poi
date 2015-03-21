# -*- coding:utf-8 -*-
__author__ = 'wuzhifan'

import logging

import smtplib
from email.mime.text import MIMEText

LOG = logging.getLogger(__name__)

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25

EMAIL_USER = 'senz_notify'
EMAIL_PWD  = 'lovesenz'

EMAIL_POSTFIX = '163.com'
FROM_ADDR = EMAIL_USER + '@' + EMAIL_POSTFIX
TO_ADDR = 'senz_notify@163.com'

EMAIL_SUBJECT = 'Senz monitor warning letter'

# handlers for monitor events
class EmailHandler(object):
    def pack_msg(self, message):
        body = '<p>' + message + '</p>' # 设置邮件正文，这里是支持HTML的

        msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容
        msg['subject'] =  EMAIL_SUBJECT# 设置邮件标题
        msg['from'] = FROM_ADDR  # 设置发送人
        msg['to'] = TO_ADDR  # 设置接收人
        return msg

    def handle(self, message):
        try:
            msg = self.pack_msg(message)

            smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            smtp.login(EMAIL_USER, EMAIL_PWD)
            smtp.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())

            return True
        except Exception ,e:
            LOG.error( 'warning email send failed : %s' % e)
            return False
        finally:
            smtp.quit()

if __name__ == '__main__':
    ob = EmailHandler()
    ob.handle("test email sendor")