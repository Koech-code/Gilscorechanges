"""
Django settings for tweetme2 project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
#from dotenv import load_dotenv
import os
from decouple import config,Csv
#load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# remember on same level as manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.25.107', '127.0.0.1','Gilscore3-dev.us-west-1.elasticbeanstalk.com', '172.31.26.131', '.cfe.sh', 'localhost']

#ALLOWED_HOSTS = ['SportsApp.eba-h3jtbm88.us-west-2.elasticbeanstalk.com']

LOGIN_URL = "/login"

MAX_TWEET_LENGTH = 240
TWEET_ACTION_OPTIONS = ["like", "unlike", "retweet"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'corsheaders',
    'rest_framework',
    'knox',
    # internal
    'accounts',
    'profiles',
    'tweets',
    'NBA',
    'NFL',
    'Laliga',
    'Bundesliga',
    'Worldcup',
    'Afcon',
    'Baseball',
    'Europa',
    'Formula1',
    'Champions',
    # media/static storage
    'storages',
    'django_extensions',

]

MIDDLEWARE = [      
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tweetme2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tweetme2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES={
   'default':{
      'ENGINE':'django.db.backends.sqlite3',
      'NAME':os.path.join(BASE_DIR,'db.sqlite3'),
   }
}

#AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static-root")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS =True


DEFAULT_RENDERER_CLASSES = [
        'rest_framework.renderers.JSONRenderer',
    ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ]
}

DEFAULT_AUTHENTICATION_CLASSES = [
     'rest_framework.authentication.SessionAuthentication',
    
]
# if DEBUG:
#     DEFAULT_RENDERER_CLASSES += [
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     ]
#     # DEFAULT_AUTHENTICATION_CLASSES += [
#     #      'tweetme2.rest_api.dev.DevAuthentication'
#     #  ]
# REST_FRAMEWORK = {
    
#     'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
#     'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
# }
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
MEDIA_URL = '/media/'


# AWS_STORAGE_BUCKET_NAME =  'gilscore'
# AWS_S3_REGION_NAME = 'us-east-1' # e.g. us-east-2
# AWS_ACCESS_KEY_ID = 'AKIAXDRNNI42RNA4JTM7'
# AWS_SECRET_ACCESS_KEY = 'TfNsmDoiVJhXH6WgjUt992Dhg72UKXDwvbO5KbEZ'

# #Tell django-storages the domain to use to refer to static files.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# #Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# #you run `collectstatic`).
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
#DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
#arn:aws:s3:::gilscore
#AKIAXDRNNI42RNA4JTM7
#TfNsmDoiVJhXH6WgjUt992Dhg72UKXDwvbO5KbEZ