from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

# UPD on 19.08.2023 - Lesson 6
# Выполним чтение данных из таблицы women БД и отобразим на главной странице
from .models import *

# UPD on 19.08.2023 - Lesson 6
# Список для главного меню
# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# UPD on 21.08.2023 - Lesson 8
# Переопределяем menu для формирования ссылок (url_name - имя маршрута)
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# Create your views here.
# UPD on 16.08.2023 - Lesson 2
# Создание функции представления
# Название функции - произвольное
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
    cats = Category.objects.all()

    # UPD on 21.08.2023 - Lesson 8
    # Переформатируем функцию представления index
    # context - произвольное название словаря
    context = {
        'posts': posts,
        # UPD on 21.08.2023 - Lesson 9
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        # UPD on 21.08.2023 - Lesson 9
        # cat_selected = 0 - на главной странице отображаются все записи
        'cat_selected': 0,
    }
    # return render(request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})

    return render(request, 'women/index.html', context=context)


# UPD on 19.08.2023 - Lesson 6
# Функция-обработчик шаблона about.xml
# Ещё нужно прописать пути в urls.py
def about(request):
    # return render(request, 'women/about.html')

    # Передача параметров в шаблоны
    # return render(request, 'women/about.html', {'title': 'О сайте'})

    # Добавим в параметры menu
    # Видно, что нарушается принцип DRY - нам нужно создать базовый шаблон base.html
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


# UPD on 17.08.2023 - Lesson 2
# Создание ещё одной функции-представления
# UPD on 17.08.2023 - Lesson 3
# Добавление возможности обработки числового параметра из запроса в представление
# <p> - тег абзаца
# Префикс f - динамическая строка
'''
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
'''


# UPD on 21.08.2023 - Lesson 8
# Добавляем функции представления для пунктов меню сайта
def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# UPD on 17.08.2023 - Lesson 3
# Добавляем функцию-обработчик исключения (exception - параметр для обработки исключения)
# HttpResponseNotFound возвращает страницу с кодом 404 (HttpResponse - 200)
# Если в какой-либо функции представления сгенерировать исключение 404,
# то произойдёт автоматическое перенаправление в данную функцию-обработчик
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# UPD on 21.08.2023 - Lesson 8
# Функция-заглушка (пока) для конкретной статьи сайта
def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


# UPD on 21.08.2023 - Lesson 9
# Функция-заглушка (пока) для конкретной категории статей сайта
'''
def show_category(request, cat_id):
    return HttpResponse(f"Отображение категории с id = {cat_id}")
'''


# UPD on 21.08.2023 - Lesson 9
# Меняем функцию для отображения категорий
# Функции index и show_category нарушают принцип DRY, позже исправим это с использованием классов представления
def show_category(request, cat_id):
    # Выбираем посты, соответствующие текущей рубрике
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    # Если категория пустая, то будем отображать страницу 404
    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)
