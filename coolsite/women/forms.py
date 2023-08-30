# UPD on 22.08.2023 - Lesson 13
# В Django существует спец. класс Form, на основе которого можно создавать классы, реализующие различные формы
# Обычно классы форм хранятся в файле forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# UPD on 30.08.2023 - Lesson 23
# Импортируем CaptchaField в проект
from captcha.fields import CaptchaField

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


# UPD on 28.08.2023 - Lesson 19
# Создадим свой класс для улучшения внешнего вида формы регистрации (расширим UserCreationForm)
class RegisterUserForm(UserCreationForm):
    # Переопределение стандартных полей формы
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Добавим поле для email
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        # Встроенная таблица auth_user из БД
        model = User
        # Названия атрибутов можно посмотреть через админ-панель и код элемента
        # fields = ('username', 'password1', 'password2')
        fields = ('username', 'email', 'password1', 'password2')
        """
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            # Почему-то к полям ввода пароля в форме регистрации стили не применяются, определим их по-другому
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }
        """


# UPD on 28.08.2023 - Lesson 20
# Добавляем класс формы для авторизации (улучшение дизайна формы)
# Класс Meta как для формы регистрации прописывать не нужно
# При необходимости можно запрашивать при авторизации и другую информацию: email, имя, фамилию и т.д.
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# UPD on 29.08.2023 - Lesson 23
# Класс, определяющий форму обратной связи (наследуется от общего класса формы Form)
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    # UPD on 30.08.2023 - Lesson 23
    # Подключаем captcha в форму
    # Проверим, как это работает
    # Отображение captcha на сайте можно менять с помощью спец. настроек
    # Существуют параметры CAPTCHA_FONT_PATH, CAPTCHA_FONT_SIZE, CAPTCHA_IMAGE_SIZE и т.д.
    # Подробнее по ссылке:
    # https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
    captcha = CaptchaField()


# UPD on 30.08.2023 - Lesson 23
"""
# Подключим django-simple-captcha
# pip install django-simple-captcha
# Настроим captcha для текущего проекта
# django-simple-captcha использует свою таблицу в БД, поэтому нужно выполнить миграцию
# python manage.py migrate
# Далее нужно подключить путь к captcha в urls.py пакета конфигураций
"""
