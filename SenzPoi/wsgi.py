# coding: utf-8

import os

import leancloud
from wsgiref import simple_server
from leancloud import Engine
from django.core.wsgi import get_wsgi_application

#from app import app
#from cloud import engine

#APP_ID = os.environ['LC_APP_ID']
#MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
#PORT = int(os.environ['LC_APP_PORT'])

#test

APP_ID = '0lffhnvekj0ndyd8f1cgwabd71yi8vs2yjt1izp1xh7xu2jw'
MASTER_KEY = 'fescseluzujxchkh6gu7huzyato9f6be1fb73pysusbpnvv1'
PORT = 3000


leancloud.init(APP_ID, master_key=MASTER_KEY)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SenzWeb.settings")

application = Engine(get_wsgi_application())


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    #app.debug = True
    server = simple_server.make_server('localhost', PORT, application)
    server.serve_forever()