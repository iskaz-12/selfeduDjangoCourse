from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
# UPD on 28.08.2023 - Lesson 20
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
# UPD on 28.08.2023 - Lesson 19
# from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
# UPD on 23.08.2023 - Lesson 15
from django.views.generic import ListView, DetailView, CreateView
# UPD on 26.08.2023 - Lesson 17
from django.contrib.auth.mixins import LoginRequiredMixin

# UPD on 22.08.2023 - Lesson 13
from .forms import *
# UPD on 19.08.2023 - Lesson 6
# Выполним чтение данных из таблицы women БД и отобразим на главной странице
from .models import *
# UPd on 26.08.2023 - Lesson 17
from .utils import *

# UPD on 19.08.2023 - Lesson 6
# Список для главного меню
# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# UPD on 21.08.2023 - Lesson 8
# Переопределяем menu для формирования ссылок (url_name - имя маршрута)
"""
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]
"""


# UPD on 27.08.2023 - Lesson 18
# Постраничная навигация в Django
"""
# Примеры рассматриваем с помощью Python Console
from django.core.paginator import Paginator
women = ['Анджелина Джоли', 'Дженнифер Лоуренс', 'Джулия Робертс', 'Марго Робби', 'Ума Турман', 'Ариана Гранде', 'Бейонсе', 'Кэтти Перри', 'Рианна', 'Шакира']
p = Paginator(women, 3) # создание пагинатора
p.count # число элементов в списке  # 10
p.num_pages # число страниц (10:3 = 4 – округление до большего)
p.page_range # итератор для перебора номеров страниц    # range(1, 5)
p1 = p.page(1) # получение первой страницы
p1.object_list  # список элементов текущей страницы # ['Анджелина Джоли', 'Дженнифер Лоуренс', 'Джулия Робертс']
p1.has_next() # имеется ли следующая страница   # True
p1.has_previous() # имеется ли предыдущая страница  # False
p1.has_other_pages() # имеются ли вообще страницы   # True (False - случай для единственной страницы)
p1.next_page_number() # номер следующей страницы    # 2
p1.previous_page_number() # номер предыдущей страницы   # Возникает ошибка
"""


# UPD on 23.08.2023 - Lesson 15
# Django позволяет создавать представления на основе классов (CBV - Class-Based View)
# Функции представления позволяют реализовать простую логику обработки запросов
# Функция index отображала статьи на главной странице сайта
# В качестве класса представления подойдёт ListView
# По умолчанию будет искаться шаблон <имя приложения>/<имя модели>_list.html
"""
class WomenHome(ListView):
    # Выбираем записи из таблицы и пытаемся отобразить в виде списка
    model = Women
    # Меняем шаблон по умолчанию на существующий
    template_name = 'women/index.html'
    # Название коллекции в шаблоне
    context_object_name = 'posts'
    # Нужно добавить заголовок вкладки в браузере
    # Существует несколько способов для этого
    # Атрибут extra_context может использоваться для передачи только статических (неизменяемых) данных
    # (например, списки передавать нельзя)
    # extra_context = {'title': 'Главная страница'}

    # Нужно определить спец. функцию для передачи динамического контекста (главного меню)
    # Т.К. В Lesson 11 ОПРЕДЕЛИЛА ПОЛЬЗОВАТЕЛЬСКИЙ ВКЛЮЧЕННЫЙ ТЕГ ДЛЯ ОТОБРАЖЕНИЯ ГЛАВНОГО МЕНЮ,
    # ТО ОНО УЖЕ ОТОБРАЖАЕТСЯ КОРРЕКТНО (НО ПРОДОЛЖУ РАБОТАТЬ СОГЛАСНО Lesson 15)
    def get_context_data(self, *, object_list=None, **kwargs):
        # Берём существующий контекст у ListView
        # **kwargs - распаковка словаря kwargs
        context = super().get_context_data(**kwargs)
        # Добавляем в context menu
        context['menu'] = menu
        # Статические данные передаём здесь
        context['title'] = 'Главная страница'
        # Нужно, чтобы пункт 'Все категории' был выбранным
        context['cat_selected'] = 0

        return context

    # Будем показывать на главной странице только те записи, у которых is_published=True
    def get_queryset(self):
        return Women.objects.filter(is_published=True)
"""


# UPD on 26.08.2023 - Lesson 17
class WomenHome(DataMixin, ListView):
    # UPD on 27.08.2023 - Lesson 18
    # Воспользуемся встроенным в ListView пагинатором
    # paginate_by = 3

    # Выбираем записи из таблицы и пытаемся отобразить в виде списка
    model = Women
    # Меняем шаблон по умолчанию на существующий
    template_name = 'women/index.html'
    # Название коллекции в шаблоне
    context_object_name = 'posts'

    # Нужно определить спец. функцию для передачи динамического контекста (главного меню)
    # Т.К. В Lesson 11 ОПРЕДЕЛИЛА ПОЛЬЗОВАТЕЛЬСКИЙ ВКЛЮЧЕННЫЙ ТЕГ ДЛЯ ОТОБРАЖЕНИЯ ГЛАВНОГО МЕНЮ,
    # ТО ОНО УЖЕ ОТОБРАЖАЕТСЯ КОРРЕКТНО (НО ПРОДОЛЖУ РАБОТАТЬ СОГЛАСНО Lesson 15)
    def get_context_data(self, *, object_list=None, **kwargs):
        # Берём существующий контекст у ListView
        # **kwargs - распаковка словаря kwargs
        context = super().get_context_data(**kwargs)

        # UPD on 26.08.2023 - Lesson 17
        c_def = self.get_user_context(title="Главная страница")

        # Словари c_def и context будут формировать нужный общий контекст
        return dict(list(context.items()) + list(c_def.items()))

    # Будем показывать на главной странице только те записи, у которых is_published=True
    """
    def get_queryset(self):
        return Women.objects.filter(is_published=True)
    """

    # UPD on 29.08.2023 - Lesson 21
    # Ленивые запросы (выполняющиеся в момент непосредственного обращения к данным)
    # хорошо использовать в случае единичного обращения к БД
    # Нужно сделать загрузку категорий и постов одним запросом. Для этого в Django имеются два полезных метода:
    # select_related(key) – "жадная" загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey;
    # prefetch_related(key) – "жадная" загрузка связанных данных по внешнему ключу key,
    # который имеет тип ManyToManyField.
    # Добавляем одновременную загрузку связанных с женщинами категорий по внешнему ключу (cat - согласно модели Women)
    # ОПТИМИЗИРУЮ ЗАПРОСЫ ДЛЯ СВОЕГО ВАРИАНТА САЙТА
    def get_queryset(self):
        # return Women.objects.filter(is_published=True).select_related('cat')
        return Women.objects.filter(is_published=True).select_related('cat', 'first_photo')


# Create your views here.
# UPD on 16.08.2023 - Lesson 2
# Создание функции представления
# Название функции - произвольное
"""
def index(request):  # HttpRequest

    # return HttpResponse("Страница приложения women.")

    # UPD on 18.08.2023 - Lesson 6
    # Нам нужно возвращать полноценную html-страницу, это можно делать следующим образом
    # return HttpResponse('''<!DOCTYPE html>
    # <html>
    # <head>
    #     <title></title>
    # </head>
    # <body>

    # </body>
    # </html>''')
    # НО это выносится за пределы приложения и организуется в виде шаблонов html-страниц

    # UPD on 19.08.2023 - пусть шаблон будет в файле index.html
    # Нужно импортировать встроенный в Django шаблонизатор
    # Функция render - встроенный шаблонизатор Django
    # Шаблоны обычно хранятся в директории templates
    # НО при сборке проекта на реальном сервере шаблоны всех приложений помещаются в единую папку templates
    # Если будет несколько шаблонов с одинаковыми именами, будет взят 1-й попавшийся
    # Принято в templates делать подкаталог и помещать туда файлы шаблонов (при сборке
    # подкаталог women перенесётся целиком в templates проекта)
    # return render(request, '')

    # Подкаталог templates не указываем, т.к. настройки импорта шаблонов есть в settings.py
    # Таким образом отделили код программы (логику) от шаблонов (представления)
    # return render(request, 'women/index.html')

    # В шаблоны можно передавать параметры через render (в виде словаря)
    # return render(request, 'women/index.html', {'title': 'Главная страница'})

    # Передача нескольких параметров
    # В браузере отображается список из элементов menu
    # return render(request, 'women/index.html', {'menu': menu, 'title': 'Главная страница'})

    # UPD on 19.08.2023 - Lesson 6
    # Women.objects.all() - чтение всех записей таблицы women_women
    # Нам даже не нужно подключаться к БД самостоятельно - это делает Django
    posts = Women.objects.all()

    # UPD on 21.08.2023 - Lesson 9
    # Получаем список категорий
    # UPD on 21.08.2023 - Lesson 11
    # Убираем cats
    # cats = Category.objects.all()

    # UPD on 21.08.2023 - Lesson 8
    # Переформатируем функцию представления index
    # context - произвольное название словаря
    context = {
        'posts': posts,
        # UPD on 21.08.2023 - Lesson 9
        # UPD on 21.08.2023 - Lesson 11
        # 'cats': cats,
        # 'menu': menu,
        'title': 'Главная страница',
        # UPD on 21.08.2023 - Lesson 9
        # cat_selected = 0 - на главной странице отображаются все записи
        'cat_selected': 0,
    }
    # return render(request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})

    return render(request, 'women/index.html', context=context)
"""


# UPD on 19.08.2023 - Lesson 6
# Функция-обработчик шаблона about.xml
# Ещё нужно прописать пути в urls.py
"""
def about(request):
    # return render(request, 'women/about.html')

    # Передача параметров в шаблоны
    # return render(request, 'women/about.html', {'title': 'О сайте'})

    # Добавим в параметры menu
    # Видно, что нарушается принцип DRY - нам нужно создать базовый шаблон base.html
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})
"""


# UPD on 26.08.2023 - Lesson 17
# Для запрета доступа к странице незарегистрированным пользователям в случае с функциями представления
# нужно использовать специальный декоратор (ошибка 404)
# @login_required
def about(request):
    # UPD on 28.08.2023 - Lesson 18
    # Пример использования класса Paginator для функций представления
    # ЧТОБЫ НЕ БЫЛО КНОПОК С НАВИГАЦИЕЙ ПО СТРАНИЦАМ В РАЗДЕЛЕ 'О сайте',
    # КОММЕНТИРУЕМ СОДЕРЖИМОЕ ДАННОЙ ФУНКЦИИ (ИЗ Lesson 18)
    """
    # http://127.0.0.1:8000/about/?page=2 - ссылка для перехода на 2-ю страницу
    # При указании в page= номера несуществующей страницы - переходим к последней
    # При указании в page= сочетания букв - переходим к первой
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    # Функция get_page() работает чуть лучше, чем page()
    page_obj = paginator.get_page(page_number)
    """

    # UPD on 28.08.2023 - Lesson 18
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})
    # return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


# UPD on 17.08.2023 - Lesson 2
# Создание ещё одной функции-представления
# UPD on 17.08.2023 - Lesson 3
# Добавление возможности обработки числового параметра из запроса в представление
# <p> - тег абзаца
# Префикс f - динамическая строка
"""
# Параметр request функции представления используется для обработки GET-запросов
# Словарь request.GET сохраняет параметры из GET-запроса
def categories(request, catid):
    # return HttpResponse("<h1>Статьи по категориям</h1>")

    # Проверка существования GET-запроса
    # if request.GET:
    #     print(request.GET)

    # Проверка существования POST-запроса
    # Обычно POST-запрос используется для работы с формами (логин-пароль и т.д.)
    if request.POST:
        print(request.POST)

    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")
    # return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat}</p>")


# UPD on 17.08.2023 - Lesson 3
def archive(request, year):
    # Http404() - генерирует исключение 404
    # UPD on 17.08.2023 - Lesson 3
    # Создадим редиректы по кодам 301 (страница перемещена на другой постоянный URL-адрес)
    # и 302 (страница временно перемещена на другой URL-адрес)
    if int(year) > 2022:
        # raise Http404()

        # redirect без доп.параметров генерирует 302
        # при параметре permanent=True - 301
        # return redirect('/')
        # return redirect('/', permanent=True)

        # Другой вариант:
        # a = redirect('/', permanent=False)
        # return a

        # Явное указание адреса, на который осуществляется перенаправление - плохая практика
        # Лучше использовать имена адресов
        # return redirect('/', permanent=False)
        return redirect('home', permanent=False)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
"""


# UPD on 21.08.2023 - Lesson 8
# Добавляем функции представления для пунктов меню сайта
"""
def addpage(request):
    return HttpResponse("Добавление статьи")
"""


# UPD on 22.08.2023 - Lesson 13
# В Django существует 2 вида форм: связанные с моделью таблицы БД или независимые
# Реализуем добавление статей на сайте с помощью независимой от модели формы
# python manage.py runserver
# Перепишем функцию addpage
# UPD on 23.08.2023 - Lesson 13
# Если не прошла проверка корректности данных, то возвращаем не пустую форму, а уже заполненную
# Если ввести недопустимые значения в поля формы, Django выведет замечание на сайте
"""
def addpage(request):
    # Добавляем переменную, ссылающуюся на экземпляр класса формы
    # form = AddPostForm()
    # Повторный показ формы (с заполненными данными)
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        # is_valid() - проверка корректности данных
        if form.is_valid():
            # отображение очищенных данных в консоли
            # print(form.cleaned_data)
            # Выполним добавление записи в БД
            try:
                # UPD on 23.08.2023 - Lesson 14
                # Для сохранения данных из формы в БД, если форма связана с ней, можно сделать проще
                # Women.objects.create(**form.cleaned_data)
                # При попытке добавления записи с занятым URL показывается ошибка (из-за метода save())
                form.save()
                return redirect('home')
            # Например, срабатывает при добавлении записи с существующим в БД слагом
            except:
                # Общая ошибка формы
                form.add_error(None, 'Ошибка добавления поста')
    # Первичный показ формы
    else:
        form = AddPostForm()
    # return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи'})
    return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
"""


# UPD on 23.08.2023 - Lesson 15
# Добавляем класс представления, реализующий форму для добавления статьи (на основе CreateView)
# Классы представления позволяют писать программный код компактнее
"""
class AddPage(CreateView):
    # Атрибут form_class указывает класс формы, который будет связан с классом представления AddPage
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # После создания поста Django автоматически перенаправляет нас по адресу
    # из get_absolute_url в соответствующем классе models.py
    # Пусть перенаправление идёт на главную страницу
    # reverse() пытается построить маршрут в момент создания экземпляра класса
    # reverse_lazy() выполняет создание маршрута, когда он понадобится
    # Можно почти везде использовать функцию reverse_lazy() вместо reverse()
    success_url = reverse_lazy('home')

    # Отображаем заголовок вкладки и меню (МЕНЮ УЖЕ ЕСТЬ ИЗ-ЗА ДОП.ЗАДАНИЯ В Lesson 11)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context
"""


# UPD on 26.08.2023 - Lesson 17
# Сделаем возможность добавления статьи доступной только для авторизованных пользователей
# Чтобы всё сработало, необходимо выйти из admin-панели
# class AddPage(DataMixin, CreateView):
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # Атрибут form_class указывает класс формы, который будет связан с классом представления AddPage
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    # Укажем адрес перенаправления для незарегистрированного пользователя
    # Прописывать конкретные URL-адреса в коде - не очень хорошая практика
    # login_url = '/admin/'
    login_url = reverse_lazy('home')
    # Генерация страницы 403 для незарегистрированных пользователей
    raise_exception = True

    # Отображаем заголовок вкладки и меню (МЕНЮ УЖЕ ЕСТЬ ИЗ-ЗА ДОП.ЗАДАНИЯ В Lesson 11)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# UPD on 23.08.2023 - Lesson 14
# Убираем form.save() из try-except
"""
def addpage(request):
    # Повторный показ формы (с заполненными данными)
    if request.method == 'POST':
        # Передаём список файлов, переданных из формы
        # form = AddPostForm(request.POST)
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('home')
    # Первичный показ формы
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
"""


def contact(request):
    return HttpResponse("Обратная связь")


# UPD on 28.08.2023 - Lesson 20
"""
def login(request):
    return HttpResponse("Авторизация")
"""


# UPD on 17.08.2023 - Lesson 3
# Добавляем функцию-обработчик исключения (exception - параметр для обработки исключения)
# HttpResponseNotFound возвращает страницу с кодом 404 (HttpResponse - 200)
# Если в какой-либо функции представления сгенерировать исключение 404,
# то произойдёт автоматическое перенаправление в данную функцию-обработчик
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# UPD on 21.08.2023 - Lesson 8
# Функция-заглушка (пока) для конкретной статьи сайта
"""
def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")
"""

# UPD on 21.08.2023 - Lesson 12
# Меняем функцию отображения статей для использования слагов в url
"""
def show_post(request, post_id):
    # Функция get_objects_or_404() возвращает запись по id или страницу 404, если запись не найдена
    post = get_object_or_404(Women, pk=post_id)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        # UPD on 21.08.2023 - Lesson 12
        # 'cat_selected': 1,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)
"""


# UPD on 23.08.2023 - Lesson 15
# Использование класса DetailView для отображения отдельной статьи
# Отображается пустая статья, т.к. для шаблона post.html не определена переменная post
"""
class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    # Переменная для слага (используемого в urls.py)
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    # Добавим меню (У МЕНЯ УЖЕ ЕСТЬ ИЗ-ЗА ДОП.ЗАДАНИЯ В Lesson 11) и название вкладки
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context
"""


# UPD on 26.08.2023 - Lesson 17
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # Переменная для слага (используемого в urls.py)
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    # Добавим меню (У МЕНЯ УЖЕ ЕСТЬ ИЗ-ЗА ДОП.ЗАДАНИЯ В Lesson 11) и название вкладки
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # заголовок title формируется на основе context,
        # созданного в методе get_context_data() базового класса DetailView
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# UPD on 22.08.2023 - Lesson 12
# Добавляем отображение слага в url
"""
def show_post(request, post_slug):
    # Страница отображается по слагу
    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)
"""


# UPD on 21.08.2023 - Lesson 9
# Функция-заглушка (пока) для конкретной категории статей сайта
"""
def show_category(request, cat_id):
    return HttpResponse(f"Отображение категории с id = {cat_id}")
"""

# UPD on 21.08.2023 - Lesson 9
# Меняем функцию для отображения категорий
# Функции index и show_category нарушают принцип DRY, позже исправим это с использованием классов представления
"""
def show_category(request, cat_id):
    # Выбираем посты, соответствующие текущей рубрике
    posts = Women.objects.filter(cat_id=cat_id)

    # UPD on 21.08.2023 - Lesson 11
    # Уберём дублирование данной функции в index и show_category с помощью пользовательских тегов
    # Django позволяет использовать два вида пользовательских тегов:
    # simple tags – простые теги;
    # inclusion tags – включающие теги.
    # Все теги в Django принято располагать в спец. подкаталоге templatetags
    # Там должен быть файл __init.py__ (чтобы каталог считался пакетом)
    # Создаём файл women_tags.py
    # UPD on 21.08.2023 - Lesson 11
    # Убираем cats
    # cats = Category.objects.all()

    # Если категория пустая, то будем отображать страницу 404
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        # UPD on 21.08.2023 - Lesson 11
        # 'cats': cats,
        # 'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)
"""


# UPD on 23.08.2023 - Lesson 15
# Создаём класс представления для отображения категорий
# Дублирование кода в классах WomenCategory и WomenHome будем убирать позже с помощью mixins
"""
class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # Для отображения страницы 404 для несуществующих категорий
    # Отображается Page not found (404)
    allow_empty = False

    # Выбираем категории, соответствующие указанному слагу
    # Через kwargs можем получить переменные маршрута из urls.py
    # cat__slug - обращаемся к полю slug таблицы Category, связанной с текущей записью
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    # Добавляем получение контекста (для отображения заголовка вкладки, установления категорий без ссылок)
    # (ИЗ-ЗА ДОП. ЗАДАНИЯ В Lesson 11 МЕНЮ ОТОБРАЖАЕТСЯ ВЕРНО, НО ПРОДЕЛАЕМ АНАЛОГИЧНЫЕ ДЕЙСТВИЯ, КАК В Lesson 15)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] - коллекция прочитанных записей
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        # Если укажем несуществующий слаг категории, то возникнет ошибка IndexError at /category/<несуществующий_слаг>/
        context['cat_selected'] = context['posts'][0].cat_id
        return context
"""


# UPD on 26.08.2023 - Lesson 17
# Весь общий код классов представлений был вынесен в DataMixin
class WomenCategory(DataMixin, ListView):
    # UPD on 28.08.2023 - Lesson 18
    # Добавляем пагинацию для категорий
    # Чтобы не было дублирования кода в WomenCategory и WomenHome - перенесём в DataMixin
    # paginate_by = 3

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # Для отображения страницы 404 для несуществующих категорий
    # Отображается Page not found (404)
    allow_empty = False

    """
    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
    """

    # UPD on 29.08.2023 - Lesson 21
    # Добавляем "жадную" загрузку категорий
    # Дублируется запрос вида:
    # SELECT ••• FROM "women_women" INNER JOIN "women_category" ON ("women_women"."cat_id" = "women_category"."id")
    # WHERE ("women_category"."slug" = '''aktrisy''' AND "women_women"."is_published")
    # ORDER BY "women_women"."id" ASC LIMIT 1
    # ОПТИМИЗИРУЮ ЗАПРОСЫ ДЛЯ СВОЕГО ВАРИАНТА САЙТА
    def get_queryset(self):
        # return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
        return (Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
                .select_related('cat', 'first_photo'))

    # Добавляем получение контекста (для отображения заголовка вкладки, установления категорий без ссылок)
    # (ИЗ-ЗА ДОП. ЗАДАНИЯ В Lesson 11 МЕНЮ ОТОБРАЖАЕТСЯ ВЕРНО, НО ПРОДЕЛАЕМ АНАЛОГИЧНЫЕ ДЕЙСТВИЯ, КАК В Lesson 15)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # UPD on 26.08.2023 - Lesson 17
        # UPD on 29.08.2023 - Lesson 21
        # Попробуем уменьшить количество запросов
        # Причина действительно в отображении названия вкладки и получении id текущей категории
        # Оптимизируем этот момент
        # ТАКЖЕ ДОПОЛНИТЕЛЬНО ПОПРОБУЮ ОПТИМИЗИРОВАТЬ ЗАПРОСЫ, СВЯЗАННЫЕ С ЗАГРУЗКОЙ ФОТОГРАФИЙ
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        """
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        """
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        # c_def = self.get_user_context(title="Главная страница")

        return dict(list(context.items()) + list(c_def.items()))


# UPD on 22.08.2023 - Lesson 12
# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: ДОБАВИТЬ ИСПОЛЬЗОВАНИЕ СЛАГОВ В ОТОБРАЖЕНИЕ URL-АДРЕСОВ КАТЕГОРИЙ
"""
def show_category(request, cat_slug):
    # Находим id по слагу из category
    cat_id = Category.objects.get(slug=cat_slug).pk

    # Выбираем посты, соответствующие текущей рубрике
    posts = Women.objects.filter(cat_id=cat_id)

    # Если категория пустая, то будем отображать страницу 404
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug,
    }

    return render(request, 'women/index.html', context=context)
"""


# UPD on 28.08.2023 - Lesson 19
# Класс представления для регистрации пользователя
# Т.к. регистрироваться будем с помощью формы, то родительский класс - CreateView (и DataMixin)
class RegisterUser(DataMixin, CreateView):
    # UserCreationForm - встроенная форма для регистрации пользователя
    # form_class = UserCreationForm
    # Используем нашу форму RegisterUserForm
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # UPD on 28.08.2023 - Lesson 20
    # Добавляем метод, авторизующий пользователя при регистрации
    # Переопределённый метод form_valid вызывается при успешной проверке формы регистрации
    def form_valid(self, form):
        # Сохраняем форму, т.е. добавляем пользователя в БД
        user = form.save()
        # Встроенная функция авторизации пользователя
        login(self.request, user)
        return redirect('home')


# UPD on 28.08.2023 - Lesson 20
# Добавляем класс представления для авторизации пользователей на сайте
# LoginView - встроенный класс с необходимой логикой для авторизации пользователя
class LoginUser(DataMixin, LoginView):
    # AuthenticationForm - стандартная форма для авторизации пользователя
    # form_class = AuthenticationForm
    # Указываем нашу форму
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    # Метод, перенаправляющий на другую страницу после прохождения авторизации
    # (вызывается, если пользователь верно ввёл логин и пароль)
    # Ссылку для перехода можно указать и в settings.py
    def get_success_url(self):
        return reverse_lazy('home')


# UPD on 28.08.2023 - Lesson 20
# Добавляем функцию представления для выхода зарегистрированного пользователя
def logout_user(request):
    logout(request)
    # redirect - перенаправление по маршруту, reverse - формирование маршрута
    return redirect('login')
