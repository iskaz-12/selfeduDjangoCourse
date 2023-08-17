from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect


# Create your views here.
# UPD on 16.08.2023 - Lesson 2
# Создание функции представления
# Название функции - произвольное
def index(request):  # HttpRequest
    return HttpResponse("Страница приложения women.")


# UPD on 17.08.2023 - Lesson 2
# Создание ещё одной функции-представления
# UPD on 17.08.2023 - Lesson 3
# Добавление возможности обработки числового параметра из запроса в представление
# <p> - тег абзаца
# Префикс f - динамическая строка

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

# UPD on 17.08.2023 - Lesson 3
# Добавляем функцию-обработчик исключения (exception - параметр для обработки исключения)
# HttpResponseNotFound возвращает страницу с кодом 404 (HttpResponse - 200)
# Если в какой-либо функции представления сгенерировать исключение 404,
# то произойдёт автоматическое перенаправление в данную функцию-обработчик
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
