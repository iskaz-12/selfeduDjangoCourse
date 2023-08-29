# UPD on 17.08.2023 - Lesson 2
# Обеспечиваем относительную независимость приложения

from django.urls import path, re_path

from .views import *

# UPD on 17.08.2023 - Lesson 3
"""
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
"""

# UPD on 19.08.2023 - Lesson 6
# Меняем url-адреса
urlpatterns = [
    # UPD on 21.08.2023 - Lesson 8
    # path('', index, name='home'),
    # UPD on 23.08.2023 - Lesson 15
    # Вызов as_view() связывает класс WomenHome с маршрутом
    # python manage.py runserver    # TemplateDoesNotExist at / (не найден шаблон по умолчанию women/women_list.html)
    path('', WomenHome.as_view(), name='home'),
    # path('home/', index, name='home'),
    path('about/', about, name='about'),
    # UPD on 21.08.2023 - Lesson 8
    # Добавляем пути пунктов меню
    # UPD on 23.08.2023 - Lesson 15
    # path('addpage/', addpage, name='add_page'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    # UPD on 28.08.2023 - Lesson 20
    # path('login/', login, name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    # UPD on 28.08.2023 - Lesson 20
    # path('logout/', LoginUser.as_view(), name='logout'),
    path('logout/', logout_user, name='logout'),
    # UPD on 28.08.2023 - Lesson 19
    # Используем класс представления RegisterUser
    # path('register/', login, name='register'),
    path('register/', RegisterUser.as_view(), name='register'),
    # UPD on 21.08.2023 - Lesson 8
    # Создание динамических url-ссылок на уровне шаблонов
    # Добавляем ссылки на статьи
    # UPD on 22.08.2023 - Lesson 12
    # Пусть в url отображается слаг статьи
    # path('post/<int:post_id>/', show_post, name='post'),
    # UPD on 23.08.2023 - Lesson 15
    # path('post/<slug:post_slug>/', show_post, name='post'),
    # AttributeError at /post/shakira/
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # slug - переменная по умолчанию при использовании класса представления
    # path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    # UPD on 21.08.2023 - Lesson 9
    # Добавляем ссылки на категории
    # path('category/<int:cat_id>/', show_category, name='category'),
    # UPD on 22.08.2023 - Lesson 12
    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: ДОБАВИТЬ ИСПОЛЬЗОВАНИЕ СЛАГОВ В ОТОБРАЖЕНИЕ URL-АДРЕСОВ КАТЕГОРИЙ
    # UPD on 23.08.2023 - Lesson 15
    # ИЗ-ЗА ДОП. ЗАДАНИЯ В Lesson 12 ИСПРАВЛЕНИЙ В ПАРАМЕТРЫ ПУТИ ВНОСИТЬ НЕ НУЖНО
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]


# UPD on 28.08.2023 - Lesson 21
# Оптимизация сайта с Django Debug Toolbar
"""
# Чтобы определить, насколько хорошо работает приложение, нужно оценивать:
# скорость работы приложения;
# нагрузку на СУБД (частоту и сложность запросов);
# корректность возвращаемых пользователю данных.
# Установим в виртуальное окружение Django Debug Toolbar
# pip install django-debug-toolbar
# Осталось настроить данный пакет применительно к сайту
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# Во вкладке SQL в Django Debug Toolbar видно, что часть запросов выполняется дважды - это не очень хорошо
# Попробуем это исправить
"""
