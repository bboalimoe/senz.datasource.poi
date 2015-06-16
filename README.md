
1.gunicorn.supervisor.conf directory must be set to the dir contains the manage.py
2.create dir that contains the your own project:RUN mkdir /app/djangoapp
3.add the whole prject files to the dir just created :ADD djangoapp/ /app/djangoapp
4.change the expose port of Docker and the listen port of nginx
