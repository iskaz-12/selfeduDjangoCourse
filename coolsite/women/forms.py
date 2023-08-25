# UPD on 22.08.2023 - Lesson 13
# В Django существует спец. класс Form, на основе которого можно создавать классы, реализующие различные формы
# Обычно классы форм хранятся в файле forms.py

from django import forms
from django.core.exceptions import ValidationError

from .models import *


# Класс, определяющий форму для добавления статьи на сайте
# Атрибуты класса - поля формы (названия совпадают с полями таблицы women)
# Прописываем только поля, которые отображаем конечному пользователю
# Можем использовать форму в функции представления
"""
class AddPostForm(forms.Form):
    # CharField - поле для ввода данных
    # title = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    # BooleanField - формирует checkbox
    is_published = forms.BooleanField()
    # ModelChoiceField - раскрывающийся список (на основе запроса к таблице БД)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
"""


# UPD on 23.08.2023 - Lesson 13
# Сделаем названия полей формы русскими
"""
class AddPostForm(forms.Form):
    # Можно добавлять оформление полей формы через виджеты
    # title = forms.CharField(max_length=255, label="Заголовок")
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
    # Сделаем поле is_published необязательным
    # Пусть чекбокс будет по умолчанию отмеченным
    # is_published = forms.BooleanField(label="Публикация")
    # is_published = forms.BooleanField(label="Публикация", required=False)
    is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
    # Сделаем отображение надписи вместо пустой категории
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")
"""


# UPD on 23.08.2023 - Lesson 14
# Создадим форму, связанную с моделью Women
# Наследуемся от класса ModelForm
# python manage.py runserver
"""
class AddPostForm(forms.ModelForm):
    # Для отображения Категория не выбрана вместо ------ создаём конструктор
    def __init__(self, *args, **kwargs):
        # Обязательно вызывается конструктор базового класса
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    # model - связь формы с моделью
    # fields - какие поля отобразить в форме ('__all__' - все поля, кроме автоматически заполняемых)
    class Meta:
        model = Women
        # На практике рекомендуется явно перечислять поля формы
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'is_published', 'cat']
        # Атрибут widgets - описание стиля оформления для каждого поля
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
"""


# UPD on 23.08.2023 - Lesson 14
# Добавим в форму поле для фото
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Women

        # UPD on 24.08.2023 - ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
        # Пробую изменить модель с помощью миграции
        # fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        fields = ['title', 'slug', 'content', 'is_published', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # UPD on 23.08.2023 - Lesson 14
    # Добавим в форму валидаторы (например, поле title должно содержать не более 200 символов)
    # SQLite3 не поддерживает проверку max_length
    # На сервере проверка осуществляется в порядке:
    # is_valid() | save()
    # Стандартные валидаторы
    # Пользовательские валидаторы
    # Название метода должно начинаться с префикса clean_
    def clean_title(self):
        # pass
        # cleaned_data содержит введённые пользователем данные
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title
