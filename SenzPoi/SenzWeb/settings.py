"""
Django settings for SenzWeb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR+'/senz/')

app_env = os.environ.get('APP_ENV', 'local')
print 'SenzWeb/settings app_env:', app_env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ifla(+65aq$bm*)*)g6aecg448b&)x3&z)nal*!^=^@z4_)wub'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'senz'
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#bugsnag config
MIDDLEWARE_CLASSES.append("bugsnag.django.middleware.BugsnagMiddleware")

test_api_key = '52936de41dfc0111c65284fdadda5bb0'

prob_api_key = 'ef167a8acd52430b091fbd275661b822'

api_key = test_api_key if app_env == 'local' or app_env == 'test' else prob_api_key

BUGSNAG = {
  "api_key": api_key,
  "project_root": BASE_DIR,
}

ROOT_URLCONF = 'SenzWeb.urls'

WSGI_APPLICATION = 'SenzWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#Django Logging
SYSLOG_HANDLER_HOST = 'localhost'
SYSLOG_UDP_PORT = 514

LOG_FOLDER = os.getcwd() + os.path.sep + 'logs'
if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

test_log_token = '304449f2-f5d7-4ee4-bf3a-ff103461f1e0'

prod_log_token = '871368b8-4c36-4da8-8f81-96caf3654c53'

log_token = test_log_token if app_env == 'local' or app_env == 'test' else prod_log_token

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'test': {
            'format' : '%(name)s %(message)s'
        },
        'simple': {
            'format': '%(lineno)s %(name)s %(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'address': (SYSLOG_HANDLER_HOST,SYSLOG_UDP_PORT), # log to syslog or rsyslog server
            'formatter': 'test',
        },
        'file':{
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FOLDER + os.path.sep + 'senz.log',
            'backupCount': 5,
            'maxBytes': '16777216', # 16megabytes(16M)
            'formatter': 'verbose'
        },
        'logentries' : {
            'level' : 'DEBUG',
            'class' : 'logentries.LogentriesHandler',
            'token' : log_token,
            'formatter' : 'verbose',
        }
    },
    'loggers': {
        'senz':{
            #'handlers': ['console', 'file'],
            'handlers': ['logentries'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}