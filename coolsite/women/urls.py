# UPD on 17.08.2023 - Lesson 2
# Обеспечиваем относительную независимость приложения

from django.urls import path, re_path

from .views import *

# UPD on 17.08.2023 - Lesson 3
'''
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
'''

# UPD on 19.08.2023 - Lesson 6
# Меняем url-адреса
urlpatterns = [
    # UPD on 21.08.2023 - Lesson 8
    path('', index, name='home'),
    # path('home/', index, name='home'),
    path('about/', about, name='about'),
    # UPD on 21.08.2023 - Lesson 8
    # Добавляем пути пунктов меню
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    # UPD on 21.08.2023 - Lesson 8
    # Создание динамических url-ссылок на уровне шаблонов
    # Добавляем ссылки на статьи
    # UPD on 22.08.2023 - Lesson 12
    # Пусть в url отображается слаг статьи
    # path('post/<int:post_id>/', show_post, name='post'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    # UPD on 21.08.2023 - Lesson 9
    # Добавляем ссылки на категории
    # path('category/<int:cat_id>/', show_category, name='category'),
    # UPD on 22.08.2023 - Lesson 12
    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: ДОБАВИТЬ ИСПОЛЬЗОВАНИЕ СЛАГОВ В ОТОБРАЖЕНИЕ URL-АДРЕСОВ КАТЕГОРИЙ
    path('category/<slug:cat_slug>/', show_category, name='category'),
]
