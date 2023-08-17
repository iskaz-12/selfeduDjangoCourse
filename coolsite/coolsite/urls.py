"""
URL configuration for coolsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from women.views import *

# UPD on 17.08.2023 - Lesson 2
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # UPD on 16.08.2023 - Lesson 2
    # Связывание функции представления с url-адресом
    # Аргументы функции path: шаблон, ссылка на функцию представления, активизирующейся на указанный запрос
    # path('women/', index),  # https://127.0.0.1:8000/women/

    # UPD on 17.08.2023 - Lesson 2
    # Подход, когда маршруты приложения прописываются в файле конфигураций urls.py нарушает
    # принцип независимости приложений. Выход - использование функции include
    # path('', index),

    # UPD on 17.08.2023 - Lesson 3
    # path('women/', include('women.urls'))   # women.urls - файл, содержащий маршруты приложения women
    path('', include('women.urls'))

    # UPD on 17.08.2023
    # path('cats/', categories),  # https://127.0.0.1:8000/cats/
]

# UPD on 17.08.2023 - Lesson 3
# Переопределяем специальный обработчик для страницы 404 (handler404 - встроен в Django)
# handler500 - ошибка сервера, handler403 - доступ запрещён, handler400 - невозможно обработать запрос
# Они начинают работать только если в settings.py DEBUG = False
handler404 = pageNotFound
