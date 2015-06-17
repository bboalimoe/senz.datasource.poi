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

RUN pip install -r requirements.txt



ADD gunicorn_conf.py /app/
ADD gunicorn.supervisor.conf /etc/supervisor/conf.d/

ADD nginx.conf /app/
ADD nginx.supervisor.conf /etc/supervisor/conf.d/


VOLUME ["/app/logs"]
EXPOSE 9010
