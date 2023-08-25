from django.contrib import admin

# Register your models here.

# UPD on 21.08.2023 - Lesson 10
# Приложение women нужно зарегистрировать для админ-панели
# Для просмотра статей на сайте админ-панель использует функцию get_absolute_url
from .models import *


# UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
# ДОБАВЛЕНИЕ ЧЕРЕЗ АДМИНИСТРАТИВНЫЙ ИНТЕРФЕЙС ЛЮБОГО КОЛИЧЕСТВА ФОТОГРАФИЙ К ЗАПИСИ В МОДЕЛИ Women
# Класс-заглушка
class WomenPhotoAdmin(admin.ModelAdmin):
    pass


# UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
# Определяем вставку для возможности редактирования модели (WomenPhoto) на странице родительской модели (Women)
class WomenPhotoInline(admin.StackedInline):
    model = WomenPhoto
    # максимальное количество форм, показанных во вставке
    max_num = 3
    # количество доп.форм в дополнение к начальным формам
    extra = 0


# UPD on 21.08.2023 - Lesson 10
# Следующим шагом добавим в списке записей дополнительные поля:
# id, title, время создания, изображение, флаг публикации
# Создаём вспомогательный класс
class WomenAdmin(admin.ModelAdmin):
    # поля записи, которые отображаются для записей в админ-панели
    # UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
    # Пытаюсь перестроить модель с помощью миграции
    # list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display = ('id', 'title', 'time_create', 'is_published')

    # поля, на которых можно перейти по ссылке
    list_display_links = ('id', 'title')
    # по каким полям можно производить поиск
    search_fields = ('title', 'content')
    # Сделаем поле Публикация редактируемым в админ-панели
    list_editable = ('is_published',)
    # Укажем поля, по которым сможем фильтровать список статей
    list_filter = ('is_published', 'time_create')
    # UPD on 22.08.2023 - Lesson 12
    # Добавляем автоматическое формирование слага на основе заголовка статьи
    # Через админ-панель заполнила БД
    prepopulated_fields = {"slug": ("title",)}

    # UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
    # Подключаем вставку
    inlines = [WomenPhotoInline, ]


# UPD on 21.08.2023 - Lesson 10
# Регистрируем модель category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    # ',' обязательна, т.к. передаём кортеж
    search_fields = ('name',)
    # UPD on 22.08.2023 - Lesson 12
    # Пусть слаг автоматически формируется из названия категории
    # prepopulated_fields - автоматическое заполнение одних полей на основе других
    prepopulated_fields = {"slug": ("name",)}


# UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
# Регистрируем модель WomenPhoto в админ-панели
admin.site.register(WomenPhoto, WomenPhotoAdmin)


# UPD on 21.08.2023 - Lesson 10
# register - встроенная функция
# admin.site.register(Women)
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
