# UPD on 17.08.2023 - Lesson 2
# Обеспечиваем относительную независимость приложения

from django.urls import path, re_path

from .views import *

# UPD on 17.08.2023 - Lesson 3
urlpatterns = [
    # path('', index),    # https://127.0.0.1:8000/

    # UPD on 17.08.2023 - Lesson 3
    # Добавляем название адреса главной страницы
    path('', index, name='home'),
    # path('home/', index, name='home'),

    # UPD on 17.08.2023 - Lesson 3
    # Создаём числовой параметр шаблона, имя параметра - произвольное (например, catid)
    # Типы данных, использующиеся в шаблонах Django: str, int, slug, uuid, path
    # Существует функция re_path(), с помощью которой можно создавать шаблоны с использованием регулярных выражений
    path('cats/<int:catid>/', categories),  # https://127.0.0.1:8000/cats/{catid}/
    # path('cats/<slug:cat>/', categories),  # https://127.0.0.1:8000/cats/{cat}/

    # (?P<...>) - синтаксис именованной группы (year - именованный параметр для части шаблона)
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]