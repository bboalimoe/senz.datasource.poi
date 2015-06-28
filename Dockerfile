FROM texastribune/supervisor
MAINTAINER tech@texastribune.org

RUN apt-get update

RUN apt-get -yq install nginx
# There's a known harmless warning generated here:
# See https://github.com/benoitc/gunicorn/issues/788

RUN pip install gunicorn==19.1.1
RUN pip install Django



# 1.every service should add the dependency to the requirements.txt



WORKDIR /app

# TOOD: move this to ancestor image?


RUN mkdir /app/run
RUN mkdir /app/djangoapp
#add the project to the /app/
ADD SenzPoi/ /app/djangoapp
WORKDIR /app/djangoapp



#dependency install


RUN pip install bugsnag

RUN pip install logentries

#numpy==1.6.2

RUN pip install pytz==2014.10

RUN pip install requests==2.5.3


RUN pip install Babel==1.3

RUN pip install eventlet==0.17.1

#greenlet==0.4.5

RUN pip install iso8601==0.1.10

RUN pip install leancloud-sdk==1.1.0

RUN pip install six==1.9.0

RUN pip install threadpool==1.2.7

RUN pip install -r requirements.txt

RUN pip install numpy
RUN apt-get install -y python-scipy

ADD gunicorn_conf.py /app/
ADD gunicorn.supervisor.conf /etc/supervisor/conf.d/

ADD nginx.conf /app/
ADD nginx.supervisor.conf /etc/supervisor/conf.d/


VOLUME ["/app/logs"]
EXPOSE 9010
