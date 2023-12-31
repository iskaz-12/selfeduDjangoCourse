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

    # UPD on 28.08.2023 - Lesson 21
    # Устанавливаем Django Debug Toolbar
    'debug_toolbar',

    # UPD on 30.08.2023 - Lesson 23
    # Устанавливаем django-simple-captcha
    'captcha',

    # UPD on 16.08.2023 - Lesson 2
    # Создание и регистрация приложения 'women'
    # допустимый, но неоптимальный вариант
    # 'women'
    # более удобный вариант
    'women.apps.WomenConfig'

    # UPD on 21.08.2023 - Lesson 10
    # Переименование нормально сработает, только если
    # в settings.py приложение зарегистрировано с использованием WomenConfig
    # ДОПОЛНИТЕЛЬНО НУЖНО В apps.py В WomenConfig УСТАНОВИТЬ ФЛАГ default = False
    # 'women',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # UPD on 28.08.2023 - Lesson 21
    # Устанавливаем Django Debug Toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'coolsite.urls'

# UPD on 19.08.2023 - Lesson 6
# Здесь указаны пути поиска шаблонов (по умолчанию Django ищет подкаталоги templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # UPD on 30.08.2023 - Lesson 24
        # Добавляем директорию, содержащую обновлённые шаблоны админ-панели
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# UPD on 21.08.2023 - Lesson 10 (работа с админ-панелью)
# 127.0.0.1:8000/admin/
# Попробуем русифицировать админ-панель
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

# UPD on 21.08.2023 - Lesson 10
# Необходимо создать суперпользователя
# python manage.py createsuperuser
# root  # имя пользователя
# root@coolsite.ru  # адрес эл.почты
# пароль стандартный
# y
# 2 зарегистрированных приложения: группы и пользователи

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# UPD on 20.08.2023 - Lesson 7
# STATIC_URL = 'static/'
STATIC_URL = '/static/'

# UPD on 20.08.2023 - Lesson 7
# К шаблонам в Django можно подключать статические файлы
# В режиме отладки Django ищет статические файлы во всех подкаталогах static
# НО в режиме эксплуатации реальный веб-сервер будет брать все статические файлы из общей папки проекта static
# Это можно осуществить с помощью команды
# python manage.py collectstatic
# Для корректной работы нужно определить 3 константы в settings.py:
# STATIC_URL – префикс URL-адреса для статических файлов;
# STATIC_ROOT – путь к общей статической папке, используемой реальным веб-сервером;
# STATICFILES_DIRS – список дополнительных (нестандартных) путей к статическим файлам,
# используемых для сбора и для режима отладки.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

# UPD on 20.08.2023 - Lesson 7
# Создаём папку static и подкаталог women (аналогично каталогу templates)
# Также создаём подкаталог css (для каскадных таблиц стилей), js (для файлов JavaScript)
# и images (для хранения изображений)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# UPD on 17.08.2023 - Lesson 4
# Задаём MEDIA_ROOT и MEDIA_URL
# BASE_DIR - текущая рабочая папка проекта
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# К URL графических файлов будет добавляться префикс media
MEDIA_URL = '/media/'

# UPD on 28.08.2023 - Lesson 20
# Определяем спец. константу для перенаправления пользователя после регистрации
# LOGIN_REDIRECT_URL = '/'

# UPD on 28.08.2023 - Lesson 21
# Устанавливаем Django Debug Toolbar
# Указываем IPs, с которыми будет работать Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# UPD on 29.08.2023 - Lesson 22
# Настраиваем кэширование на уровне файловой системы
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # 'LOCATION': 'c:/foo/bar',
        # Определим путь к корневой папке кэша
        'LOCATION': os.path.join(BASE_DIR, 'coolsite_cache'),
    }
}
