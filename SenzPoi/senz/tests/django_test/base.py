__author__ = 'wuzhifan'

import os
import sys
import logging
import unittest

from django.test import Client


FILE = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(FILE))))
logging.basicConfig(filename=os.path.join(FILE,'log.txt'),level=logging.INFO)

from senz.db.avos import avos_manager

''' run test in command line. eg:

        python manage.py test senz.tests.django_test.test_places
'''

class SenzTestBase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.avos_manager = avos_manager.AvosManager()
