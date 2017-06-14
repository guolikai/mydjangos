#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-23 by Author:GuoLikai


"""
Django settings for Stark project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x=b9fh*-bcn0l)daobv6v=ksru+(p83ir$!3g+&@d7)+%xw4s2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Wolf',     #自定义用户系统
    'Arya',     #salt源码实现
    'Sansa',    #CMDB--->Configuration Management Database 配置管理数据库
    'Robb',     #分布式监控系统
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Stark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Stark.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stark',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '172.16.1.68',
        'PORT': '3306',
    }
}
'''
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
#LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'templates/statics/'),
    )
# for Arya
SALT_CONFIG_FILES_DIR = "%s/Arya/salt_configs" % BASE_DIR
SALT_PLUGINS_DIR = "%s/Arya/plugins" % BASE_DIR

AUTH_USER_MODEL = 'Wolf.UserProfile'   #用户自定义认证，替换原Django认证系统
#Django 内建的User 模型可能不适合某些类型的项目。例如，在某些网站上使用邮件地址而不是用户名作为身份的标识可能更合理。
#Django 允许你通过AUTH_USER_MODEL 设置覆盖默认的User 模型， 其值引用一个自定义的模型。
TOKEN_TIMEOUT = 120

LOGIN_URL = '/login/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# for Robb
REDIS_CONN = {
    'HOST': '172.16.1.101',
    'PORT': 6379,
    'PASSWD':''
}

#all the triggers will be published to this channel
TRIGGER_CHAN = 'trigger_evnet_channel'
#all latest monitor data will save under this key in redis

STATUS_DATA_OPTIMIZATION = {
    'latest':[0,600],#[间隔,存数据量]
    '10mins':[600,600], #4days
    '30mins':[1800,600],#14days
    '60mins':[3600,600],#25days
}

REPORT_LATE_TOLERANCE_TIME = 10 #allow service report late than monitor interval no more than defined seconds.

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'glk0518@163.com'
EMAIL_HOST_PASSWORD = 'shouquan123'
DEFAULT_FROM_EMAIL = 'glk0518@163.com>'