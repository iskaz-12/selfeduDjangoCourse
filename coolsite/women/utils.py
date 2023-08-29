# UPD on 25.08.2023 - Lesson 17 (Mixins)
# В Python, благодаря наличию механизма множественного наследования,
# примеси (mixins) можно добавлять в виде отдельного базового класса
# Класс DataMixin лучше передавать первым в списке наследования
# (т.к. в нем могут быть атрибуты и методы, которые используются конструктором следующего класса)
# Обычно в Django все вспомогательные классы объявляют в отдельном файле приложения utils.py
from django.db.models import Count

from .models import *

# UPD on 28.08.2023 - Lesson 19
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:
    # UPD on 28.08.2023 - Lesson 18
    # Переносим параметризацию пагинации в mixin
    # paginate_by = 3
    # Если страниц будет слишком много, то лучше отображать только часть в навигации

    # UPD on 29.08.2023 - Lesson 21
    # Попробуем оптимизировать SQL-запрос:
    # SELECT ••• FROM "women_category" WHERE "women_category"."id" = '1' LIMIT 21
    # Количество запросов такого вида увеличилось (смотрим в index.html)
    # paginate_by = 2
    paginate_by = 20

    # Если весь список умещается на одну страницу, то номера страницы отображать не нужно
    # paginate_by = 30

    # Дублируется context, передаваемый в разные шаблоны
    def get_user_context(self, **kwargs):
        # создаём словарь именованных параметров, переданных через аргументы функции
        context = kwargs
        # формируем список категорий
        # cats = Category.objects.all()

        # UPD on 26.08.2023 - Lesson 17
        # Не будем отображать рубрики, в которых нет ни одной статьи
        # С помощью метода annotate добавляем дополнительный атрибут - количество записей в рубриках
        cats = Category.objects.annotate(Count('women'))

        # context['menu'] = menu

        # UPD on 26.08.2023 - Lesson 17
        # Пусть пункт 'Добавить статью' видят только авторизованные пользователи
        # МНЕ НУЖНО ПРОПИСАТЬ УТОЧНЕНИЕ ДЛЯ МЕНЮ В ПОЛЬЗОВАТЕЛЬСКОМ ТЕГЕ (ДОП.ЗАДАНИЕ ИЗ Lesson 11)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        # передаём категории в context
        context['cats'] = cats
        # Если в kwargs не передаём cat_selected, то переопределяем cat_selected по умолчанию
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
