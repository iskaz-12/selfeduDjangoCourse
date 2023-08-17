from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# UPD on 16.08.2023 - Lesson 2
# Создание функции представления
# Название функции - произвольное
def index(request):  # HttpRequest
    return HttpResponse("Страница приложения women.")


# UPD on 17.08.2023 - Lesson 2
# Создание ещё одной функции-представления
def categories(request):
    return HttpResponse("<h1>Статьи по категориям</h1>")
