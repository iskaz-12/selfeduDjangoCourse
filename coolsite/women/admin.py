from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

# UPD on 21.08.2023 - Lesson 10
# Приложение women нужно зарегистрировать для админ-панели
# Для просмотра статей на сайте админ-панель использует функцию get_absolute_url
from .models import *


# UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
# ДОБАВЛЕНИЕ ЧЕРЕЗ АДМИНИСТРАТИВНЫЙ ИНТЕРФЕЙС ЛЮБОГО КОЛИЧЕСТВА ФОТОГРАФИЙ К ЗАПИСИ В МОДЕЛИ Women
# Класс-заглушка
# UPD on 31.08.2023 - Lesson 24
# ДОПОЛНИТЕЛЬНО НАСТРОИМ ОТОБРАЖЕНИЕ МИНИАТЮР И ДЛЯ ДАННОЙ ПАНЕЛИ
class WomenPhotoAdmin(admin.ModelAdmin):
    # pass

    list_display = ('id', 'women', 'get_html_photo')

    list_display_links = ('id', 'women')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"

    fields = ('photo', 'get_html_photo', 'women')
    readonly_fields = ('get_html_photo',)


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
    # list_display = ('id', 'title', 'time_create', 'is_published')
    # UPD on 31.08.2023 - Lesson 24
    # ДОБАВЛЯЕМ В ОТОБРАЖЕНИЕ first_photo ИЗ WomenPhoto
    # Можно с помощью функций переопределять отображение по умолчанию
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')

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

    # UPD on 31.08.2023 - Lesson 24
    # Добавим миниатюру при редактировании поста
    # Укажем редактируемые поля
    # fields = ('title', 'slug', 'cat', 'content', 'photo', 'is_published')
    # fields = ('title', 'slug', 'cat', 'content', 'photo', 'is_published', 'time_create', 'time_update')
    # fields = ('title', 'slug', 'cat', 'content', 'is_published')
    # fields = ('title', 'slug', 'cat', 'content', 'is_published', 'time_create', 'time_update')
    fields = ('title', 'slug', 'cat', 'content', 'is_published', 'get_html_photo', 'time_create', 'time_update')
    # Укажем нередактируемые поля
    # Только после этого можем добавить их в fields
    # Миниатюру прописываем как поле только для чтения
    # readonly_fields = ('time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    # Существуют и другие параметры ModelAdmin
    # save_on_top - отображает панель сохранения изменений и вверху страницы
    save_on_top = True

    # UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
    # Подключаем вставку
    inlines = [WomenPhotoInline, ]

    # UPD on 31.08.2023 - Lesson 24
    # Следующий шаг - пусть фото (а не пути к ним) отображаются в админ панели
    # Т.К. ПЕРЕОПРЕДЕЛЯЛА ФОТО В ОТДЕЛЬНОЙ ТАБЛИЦЕ, ТО ПРОПИСЫВАТЬ ОТОБРАЖЕНИЕ ПРИДЁТСЯ ПО-ДРУГОМУ
    # Параметр object - нестандартный, ссылается на текущую запись списка
    # mark_safe - добавляет фильтр safe к фрагменту html-кода (html-теги воспринимаются как теги)
    # Не у всех постов есть фотографии - нужна проверка на существование фото
    def get_html_photo(self, object):
        # if object.photo:
        #   return mark_safe(f"<img src='{object.photo.url}' width=50>")

        if object.first_photo:
            if object.first_photo.photo:
                return mark_safe(f"<img src='{object.first_photo.photo.url}' width=50>")

    # UPD on 31.08.2023 - Lesson 24
    # Определяем название поля с фотографией
    get_html_photo.short_description = "Миниатюра"


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


# UPD on 30.08.2023 - Lesson 24
# Настройка админ-панели
"""
# Попробуем изменить стиль оформления админ-панели
# С помощью Django Debug Toolbar смотрим, какие шаблоны используются при формировании админ-панели
# Пример пути: C:\\RMR Digital Technologies\\Django Tutorial\\selfedu Youtube Course\\lesson1_site\\lesson1_venv\\
# Lib\\site-packages\\django\\contrib\\admin\\templates\\admin\\base_site.html
# Могли бы внести изменения во встроенный шаблон base_site.html, но это не лучшая практика,
# все создающиеся при установке Django шаблоны лучше оставлять без изменений
# Переопределять нужно непосредственно в нашем проекте
# Создаём в корне проекта coolsite папку templates, а в ней - подкаталог admin
# Если в coolsite/admin разместить файл base_site.html, то он будет переопределять встроенный в Django файл 
# (т.к. Django будет искать шаблоны сначала в нестандартных подкаталогах, а затем - в каталогах приложений)
"""


# UPD on 31.08.2023 - Lesson 24
# Меняем название вкладки в браузере и заголовок в header админ-панели
# Полный список атрибутов admin.site - в документации
admin.site.site_title = 'Админ-панель сайта о женщинах'
admin.site.site_header = 'Админ-панель сайта о женщинах 2'
