# UPD on 17.08.2023 - Lesson 2
# Обеспечиваем относительную независимость приложения

from django.urls import path

from .views import *

urlpatterns = [
    path('', index),    # https://127.0.0.1:8000/women/
    path('cats/', categories),  # https://127.0.0.1:8000/women/cats/
]