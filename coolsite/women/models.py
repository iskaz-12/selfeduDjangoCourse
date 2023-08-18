# UPD on 17.08.2023 - Lesson 4
# Модуль models содержит базовые классы моделей, на основе которых можно создавать свои модели БД
from django.db import models


# Create your models here.
# UPD on 17.08.2023 - Lesson 4
# Создаём класс Women (название м.б. произвольным), он соответствует таблице Women в базе данных
# Наследуем данный класс от базового класса Model, определяющего механизмы создания классов моделей
# Поле id уже присутствует в классе Model, его доопределять не нужно
# По умолчанию, последовательность полей в таблице будет такой же, как в модели
class Women(models.Model):
    # UPD on 17.08.2023 - Lesson 4
    # Через классы ...Field определяются поля таблицы в базе данных
    title = models.CharField(max_length=255)
    # TextField - большое текстовое поле
    # blank=True - поле может быть пустым
    content = models.TextField(blank=True)
    # upload_to - определяет, в какие каталоги/подкаталоги загружаются фото
    # Можно использовать шаблоны папок
    # Для использования ImageField нужно определить доп.константы: MEDIA_ROOT и MEDIA_URL
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    # auto_now_add=True - принимает текущее время в момент добавления записи и больше никогда не меняется
    time_create = models.DateTimeField(auto_now_add=True)
    # auto_now=True - поле меняется каждый раз, когда мы изменяем что-то в текущей записи
    time_update = models.DateTimeField(auto_now=True)
    # default - значение поля по умолчанию
    is_published = models.BooleanField(default=True)

# UPD on 17.08.2023 - Lesson 4
# Чтобы создать таблицу в БД нужно создать и выполнить миграции
# Миграции - модули Python с командами на уровне ORM-интерфейса для создания таблиц с определённой структурой
# При выполнении файла миграций в БД автоматически создаются новые
# или обновляются существующие таблицы и связи между ними
# Файлы миграций будут добавляться в папку migrations
# Файлы миграций можно воспринимать как контроллеры версий
# В реальной практике изменения структур таблиц лучше избегать
# Порядок команд в терминале:
# python manage.py makemigrations
# python -m pip install Pillow (опционально)
# python manage.py makemigrations (опционально)
# python manage.py sqlmigrate women 0001 (women - название модели, 0001 - порядковый номер миграции)
# (будет создана таблица women_women (название приложения_название модели))
# python manage.py migrate (помимо таблицы women_women будут созданы и другие таблицы (для администрирования и т.д.))

# UPD on 17.08.2023 - Lesson 5
# Если в терминале выполнить команду
# python manage.py shell
# то откроется консоль фреймворка Django
# В ней можно работать с командами ORM

# UPD on 18.08.2023 - Lesson 5
# Последовательность выполнения команд в InteractiveConsole:
# from women.models import Women    # импорт модели
# Women(title='Анджелина Джоли', content='Биография Анджелины Джоли')   # создание записи в таблице women_women
# (значения остальных полей задаются по умолчанию, для photo в консоли Django - пустая строка)
# (запись не была добавлена в таблицу, т.к. модели в Django по умолчанию ленивые,
# т.е. при создании экземпляра класса запись не создаётся сразу же)
# w1 = _    # _ - спец. переменная в консоли Django, которая сохраняет в себе последнее действие
# (в данном случае - ссылку на последний созданный к этому моменту объект)
# w1.save() # сохранение значения из w1 в таблицу
# (<Women: Women object (None)>, значение None показывает, что запись не добавлена в таблицу (id=None))
# w1    # (<Women: Women object (1)>, т.е. id=1)
# w1.id # Можем обращаться к значениям полей записи в консоли Django
# w1.title
# w1.time_create
# w1.pk # часто используемый атрибут объектов модели (pk - синоним id)
# (по соглашению в Django определили атрибут pk, который всегда доступен и содержит номер текущей записи/None)
# from django.db import connection  # рассмотрим sql-запрос для создания данной записи
# connection.queries
# TO DO...
