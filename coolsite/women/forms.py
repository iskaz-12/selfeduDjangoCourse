# UPD on 22.08.2023 - Lesson 13
# В Django существует спец. класс Form, на основе которого можно создавать классы, реализующие различные формы
# Обычно классы форм хранятся в файле forms.py

from django import forms
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
