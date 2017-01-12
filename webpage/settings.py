"""
Django settings for webpage project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from .social_auth import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('webpage/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

# DEBUG = bool(os.environ.get('DJANGO_DEBUG', False))


ADMINS = (('Misha86', 'mishaelitzem2@rambler.ru'),)

ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = [os.environ.get('DJANGO_HOSTS', "*")]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # install apps
    'social.apps.django_app.default',
    # other django apps
    'django.contrib.humanize',
    # my apps
    'message',
    'comment.apps.CommentConfig',
    ]

MIDDLEWARE_CLASSES = [
    # for django-log-request
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # for django-social-auth
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    ]

ROOT_URLCONF = 'webpage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'message', 'templates', 'message'),
            os.path.join(BASE_DIR, 'comment', 'templates', 'comment'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # for django-social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                ],
            },
        },
    ]

WSGI_APPLICATION = 'webpage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
from .db_password import db_password

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'webpage',                                     # Or path to database file if using sqlite3.
        'USER': 'postgres',
        'PASSWORD': db_password,
        'HOST': 'localhost',    # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',             # Set to empty string for default.
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# 'ru-Ru'
# 'uk-Uk'
# 'en-En'

LANGUAGE_CODE = 'uk-Uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'comment', 'static', 'comment'),
    os.path.join(BASE_DIR, 'message', 'static', 'message'),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

LOGIN_URL = 'message:enter'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'message:list'


import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
LOG_REQUESTS = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            },
        },
    'loggers': {
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        }
}