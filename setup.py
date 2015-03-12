from distutils.core import setup

setup(
    name='SeventService',
    version='1.0.0',
    packages=['senz', 'senz.poi', 'senz.common', 'senz.location_recognition',
              'senz.activity_user_mapping', 'SenzWeb', 'activity_spider', 'scrapy_spider'],
    url='http://laboon.io',
    license='GPL license',
    author='bboalimoe',
    author_email='bboalimoe@gmail.com',
    description='senzseventtrackerservice'

)
