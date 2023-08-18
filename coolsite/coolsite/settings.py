"""
Django settings for coolsite project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# UPD on 17.08.2023 - Lesson 4
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cyijmny_p^%q6a@7vdp@xf2ibbo15(0at$$gdh-qj1mpgc)zgc'

# UPD on 17.08.2023 - Lesson 3
# Процесс отладки определяется именно в данном файле настроек settings.py

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# UPD on 17.08.2023 - Lesson 3
# Если DEBUG = False, то нужно настроить коллекцию ALLOWED_HOSTS
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # UPD on 16.08.2023 - Lesson 2
    # Создание и регистрация приложения 'women'
    # допустимый, но неоптимальный вариант
    # 'women'
    # более удобный вариант
    'women.apps.WomenConfig'
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

ROOT_URLCONF = 'coolsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'coolsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# UPD on 17.08.2023 - Lesson 4
# Здесь хранятся текущие настройки базы данных
# Для работы с другими СУБД (PostgreSQL, MySQL и т.д.) здесь нужно подключить нужный сервер Django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# UPD on 17.08.2023 - Lesson 4
# Задаём MEDIA_ROOT и MEDIA_URL
# BASE_DIR - текущая рабочая папка проекта
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# К URL графических файлов будет добавляться префикс media
MEDIA_URL = '/media/'
