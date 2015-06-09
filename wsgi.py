# coding: utf-8

import os

import leancloud
from wsgiref import simple_server

from app import app
from cloud import engine

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])


leancloud.init(APP_ID, master_key=MASTER_KEY)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SenzWeb.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    app.debug = True
    server = simple_server.make_server('localhost', PORT, application)
    server.serve_forever()