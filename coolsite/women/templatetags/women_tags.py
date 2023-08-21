# UPD on 21.08.2023 - Lesson 11
from django import template
from women.models import *

# UPD on 21.08.2023 - Lesson 11
# УПРАЖНЕНИЕ: ОПРЕДЕЛИТЬ ГЛАВНОЕ МЕНЮ ЧЕРЕЗ ПОЛЬЗОВАТЕЛЬСКИЕ ТЕГИ
from women.views import *

# Через класс Library происходит регистрация собственных шаблонных тегов
register = template.Library()


# Опишем функцию для работы простого тега
# Название тега придумываем сами
# Нужно связать функцию с тегом, для этого используем декоратор
# Если мы хотим, чтобы тег был доступен в шаблонах по другому имени, то используем name в декораторе
# @register.simple_tag()
@register.simple_tag(name='getcats')
# Можно передавать параметры в пользовательские теги
# def get_categories():
def get_categories(filter=None):
    # return Category.objects.all()
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


# UPD on 21.08.2023 - Lesson 11
# Включающий тег позволяет дополнительно формировать свой собственный шаблон на основе
# некоторых данных и возвращать фрагмент HTML-страницы
# Для тегов шаблонов можно создать отдельный подкаталог, но здесь так делать не будем
"""
@register.inclusion_tag('women/list_categories.html')
def show_categories():
    cats = Category.objects.all()
    return {"cats": cats}
"""


# UPD on 21.08.2023 - Lesson 11
# Передаём параметры в тег
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}


# UPD on 21.08.2023 - Lesson 11
# ОПРЕДЕЛИМ ПОЛЬЗОВАТЕЛЬСКИЙ ВКЛЮЧЕННЫЙ ТЕГ ДЛЯ ОТОБРАЖЕНИЯ МЕНЮ
# ШАБЛОН - list_menu.html
@register.inclusion_tag('women/list_menu.html')
def show_menu():
    return {"menu": menu}