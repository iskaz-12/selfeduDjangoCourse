# UPD on 17.08.2023 - Lesson 4
# Модуль models содержит базовые классы моделей, на основе которых можно создавать свои модели БД
from django.db import models
from django.urls import reverse


# UPD on 23.08.2023 - Lesson 16 (Основы ORM Django за час)
"""
# Команды для выполнения в командной строке:
python manage.py shell
from women.models import *
Women.objects.all() # сортировка в соответствии с классом Meta модели Women
Women.objects.all()[:5] # первые 5 записей (отбор на уровне SQL-запроса)
from django.db import connection
connection.queries  # ... LIMIT 5
Women.objects.all()[3:8]
connection.queries  # ... LIMIT 5 OFFSET 3
# order_by() - сортировка
Women.objects.order_by('pk')
Women.objects.order_by('-pk')   # обратный порядок сортировки
Women.objects.all().reverse()   # reverse() - обратный порядок относительно стандартного
Women.objects.all()
Women.objects.filter(pk__lte=2) # возвращается QuerySet
Women.objects.get(pk=2) # возвращается экземпляр модели Women
# Обработка данных связанных таблиц
w = Women.objects.get(pk=1)
# Доступные свойства:
# w.title, …, w. is_published – значения полей записи таблицы women;
# w.pk, w.id – идентификаторы записи (первичный ключ);
# w.cat_id – идентификатор рубрики (внешний ключ);
# w.cat – объект класса Category, хранящий данные записи с id = cat_id.
w.cat   # ссылка на категорию - <Category: Актрисы> # из-за перегруженного в Category метода __str__
w.cat.name  # 'Актрисы'
# Получение связанных данных - только в момент обращения к ним
connection.queries
w.cat.name
# Используя первичную модель Category, получим все связанные с ней посты из вторичной модели Women
# У любой первичной модели по умолчанию создаётся объёкт <вторичная модель>_set, 
# с помощью которого можно выбирать все связанные записи
c = Category.objects.get(pk=1)
c   # <Category: Актрисы>
c.women_set # ссылка на объект
c.women_set.all()
# Другое название для women_set
exit()
python manage.py shell
from women.models import *
c = Category.objects.get(pk=2)
c.get_posts.all()
c.get_posts.filter(is_published=True)
exit()
# Фильтры полей (lookups)
python manage.py shell
# Уже известные нам lookups 
# <имя атрибута>__gte – сравнение больше или равно (>=);
# <имя атрибута>__lte – сравнение меньше или равно (<=).
from women.models import *
Women.objects.filter(pk__gt=2)
# lookups contains (поиск, чувствительный к регистру) и icontains (поиск, нечувствительный к регистру)
Women.objects.filter(title__contains='ли')
from django.db import connection
connection.queries  # ... WHERE ... "title" LIKE \'%ли%\' ...
Women.objects.filter(title__icontains='ЛИ') # <QuerySet []>
# SQLite3 не поддерживает регистронезависимый поиск для не ASCII-символов
# В случае с латинскими символами в SQLite поиск всегда проходит как регистронезависимый
# Фильтр in (указание выбираемых значений через список)
Women.objects.filter(pk__in=[2,5,11,12])
Women.objects.filter(pk__in=[2,5,11,12], is_published=True) # объединение условий по and
# Применение in для внешнего ключа
Women.objects.filter(cat__in=[1, 2])
Women.objects.filter(cat_id__in=[1, 2])
cats = Category.objects.all()
Women.objects.filter(cat__in=cats)
# Использование класса Q (логическое ИЛИ или НЕ в условии)
# Совместные с классом Q операторы: 
# & - логическое И (приоритет 2);
# | - логическое ИЛИ (приоритет 3);
# ~ - логическое НЕ (приоритет 1).
from django.db.models import Q
Women.objects.filter(pk__lt=5, cat_id=2)    # <QuerySet []> (т.к. записи с 1-й по 4-ю относятся к 1-й рубрике)
Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2))
Women.objects.filter(Q(pk__lt=5) & Q(cat_id=2)) # <QuerySet []>
Women.objects.filter(~Q(pk__lt=5) | Q(cat_id=2))    # ~Q(pk__lt=5) - взять записи с pk>=5 
Women.objects.filter(~Q(pk__lt=5) & Q(cat_id=2))
# Быстрое получение записей из таблицы
Women.objects.first()   # <Women: Ариана Гранде> (берётся 1-я запись в соответствии с порядком сортировки модели)
Women.objects.all()
Women.objects.order_by('pk').first()    # <Women: Анджелина Джоли>
Women.objects.order_by('-pk').first()   # <Women: Ариана Гранде>
Women.objects.order_by('pk').last() # <Women: Ариана Гранде>
Women.objects.order_by('-pk').last()    # <Women: Анджелина Джоли>
Women.objects.filter(pk__gt=5).last()   # <Women: Ариана Гранде>
# Получение записи по дате
# Существуют методы: 
# latest() – выбор записи с самой поздней датой (наибольшей);
# earliest() – выбор записи с самой ранней датой (наименьшей).
Women.objects.latest('time_update') # <Women: Ариана Гранде>
Women.objects.earliest('time_update')   # <Women: Анджелина Джоли>
# Методы earliest/latest работают без учёта сортировки
Women.objects.order_by('title').earliest('time_update') # <Women: Анджелина Джоли>
Women.objects.order_by('title').latest('time_update')   # <Women: Ариана Гранде>
# Выбор записи относительно текущей (по дате)
w = Women.objects.get(pk=7)
w   # <Women: Бейонсе>
w.get_previous_by_time_update() # <Women: Ариана Гранде>
# суффикс time_update – название поля, по которому определяется предыдущая запись
w.get_next_by_time_update() # <Women: Кэтти Перри>
# В данных методах можно дополнительно указывать условия выборки следующей/предыдущей записи
w.get_next_by_time_update(pk__gt=10)    # <Women: Анастасия Эшли>
# Методы exists() и count()
# exists() – проверка существования записи;
# count() – получение числа записей.
# Добавим новую категорию - спортсменки
Category.objects.create(name='Спортсменки', slug='sportsmenki') # <Category: Спортсменки>
c3 = Category.objects.get(pk=3)
c3  # <Category: Спортсменки>
c3.women_set.exists()   # False (нет ни одной записи, связанной со спортсменками)
c2 = Category.objects.get(pk=2)
c2.women_set.exists()   # True
c2.women_set.count()    # 7
c3.women_set.count()    # 0
# Методы exists() и count() применяются к любой выборке
Women.objects.filter(pk__gt=4).count()  # 10
# Выборка записей по полям связанных моделей
Women.objects.filter(cat__slug='aktrisy')
# Параметр cat__slug сформирован по правилу: <имя первичной модели>__<название поля первичной модели>
Women.objects.filter(cat__in=[1])   # результат аналогичен результату предыдущей команды
Women.objects.filter(cat__name='Певицы')    # происходит объединение записей из 2 таблиц
connection.queries  # ... INNER JOIN "women_category" ON ("women_women"."cat_id" = "women_category"."id")
# WHERE "women_category"."name" = \'Певицы\' ...
Women.objects.filter(cat__name='Певицы')
# После имени поля можно дополнительно указывать фильтры
Women.objects.filter(cat__name__contains='ы')   # актрисы и певицы
Women.objects.filter(cat__name__contains='цы')  # певицы
# Выберем все категории, которые связаны с записями вторичной модели Women, содержащие 'ли'
Category.objects.filter(women__title__contains='ли')
# <QuerySet [<Category: Актрисы>, <Category: Актрисы>, <Category: Актрисы>, <Category: Певицы>]>
# Для получения уникальных категорий используем метод distinct()
Category.objects.filter(women__title__contains='ли').distinct() # <QuerySet [<Category: Актрисы>, <Category: Певицы>]>
# Некоторые функции агрегации
# Функции агрегации в SQL-запросах выполняются в последнюю очередь (после WHERE)
# Пример - функция count()
Women.objects.count()   # 14
# Остальные агрегирующие команды прописываем в спец. методе aggregate()
Women.objects.aggregate(Min('cat_id'))  # NameError: name 'Min' is not defined
from django.db.models import *
Women.objects.aggregate(Min('cat_id'))  # {'cat_id__min': 1}
Women.objects.aggregate(Min('cat_id'), Max('cat_id'))   # {'cat_id__min': 1, 'cat_id__max': 2}
# Названия ключей можно менять
Women.objects.aggregate(cat_min=Min('cat_id'), cat_max=Max('cat_id'))   # {'cat_min': 1, 'cat_max': 2}
# С агрегирующими значениями можно выполнять различные математические операции
Women.objects.aggregate(res=Sum('cat_id') - Count('cat_id'))    # {'res': 7}
Women.objects.aggregate(res=Avg('cat_id'))  # {'res': 1.5}
# Агрегацию можно применять только к некоторым записям
Women.objects.filter(pk__gt=4).aggregate(res=Avg('cat_id')) # {'res': 1.7}
# Выбор записи и её конкретных полей
w = Women.objects.get(pk=1)
w.title # 'Анджелина Джоли'
w.slug  # 'andzhelina-dzholi'
connection.queries  # После SELECT перечисляются все поля таблицы women
# Для указания нужных полей в выборке используется метод values()
Women.objects.values('title', 'cat_id').get(pk=1)   # {'title': 'Анджелина Джоли', 'cat_id': 1}
connection.queries  # Выбирается всего 2 поля в SELECT
# Можно использовать связанные данные
Women.objects.values('title', 'cat__name').get(pk=1)    # {'title': 'Анджелина Джоли', 'cat__name': 'Актрисы'}
connection.queries  # ... FROM "women_women" INNER JOIN "women_category" 
# ON ("women_women"."cat_id" = "women_category"."id") ...
w = Women.objects.values('title', 'cat__name')
w   # <QuerySet [{'title': 'Ариана Гранде', 'cat__name': 'Певицы'}, ...]>
connection.queries  # выполнился всего 1 sql-запрос
for p in w:
     print(p['title'], p['cat__name'])
connection.queries  # выполнился всего 1 sql-запрос
# Группировка записей и агрегирование (метод annotate())
Women.objects.values('cat_id').annotate(Count('id'))
# <QuerySet [{'cat_id': 1, 'id__count': 7}, {'cat_id': 2, 'id__count': 7}]>
# Аналог SQL-запроса: SELECT count(id) FROM women GROUP BY cat_id
# У МЕНЯ ЗАПРОС ВЫПОЛНИЛСЯ НОРМАЛЬНО СРАЗУ ПОЧЕМУ-ТО...
# НО В УРОКЕ РЕКОМЕНДУЮТ УБРАТЬ ordering ИЗ Meta (СДЕЛАЮ ТАК)
exit()
# ЗАКОММЕНТИРУЕМ ordering В Meta
python manage.py shell
from women.models import *
from django.db.models import *
from django.db import connection
Women.objects.values('cat_id').annotate(Count('id'))
# <QuerySet [{'cat_id': 1, 'id__count': 7}, {'cat_id': 2, 'id__count': 7}]>
Women.objects.annotate(Count('cat'))    # группировка идёт по всем полям
# Если для первичной модели Category вызвать метод annotate и в агрегирующей функции Count передать
# в аргументы 'women', то получим все рубрики
c = Category.objects.annotate(Count('women'))
c   # <QuerySet [<Category: Актрисы>, <Category: Певицы>, <Category: Спортсменки>]>
c[0].women__count   # 7 (количество записей, связанных с рубрикой)
c[1].women__count   # 7
c = Category.objects.annotate(total=Count('women'))
c[0].total  # 7
len(c)  # 3
# Выведем рубрики, где есть записи
c = Category.objects.annotate(total=Count('women')).filter(total__gt=0)
c   # <QuerySet [<Category: Актрисы>, <Category: Певицы>]>
# Класс F
Women.objects.filter(pk__lte='cat_id')  # такая запись приведёт к ошибке
# Чтобы такая операция стало допустимой, нужно использовать спец. класс F
from django.db.models import F
# Сравним pk с полем cat_id текущей записи
Women.objects.filter(pk__gt=F('cat_id'))    # получим все записи, кроме 1-й
connection.queries  # ... WHERE "women_women"."id" > ("women_women"."cat_id") ...
Women.objects.filter(pk__gt=F('cat_id'))
# Пусть в таблице women есть поле views - число просмотров записи
#views
# Увеличим значение views конкретной записи на 1
Women.objects.filter(slug='bejonse').update(views=F('views')+1)
# Возникает ошибка из-за отсутствия поля views в таблице women
# Можно сделать так
w = Women.objects.get(pk=1)
w   # <Women: Анджелина Джоли>
w.views = F('views')+1
w.save()
# Можно также было бы использовать
w.views += 1
# Но документация Django не рекомендует так делать из-за риска возникновения коллизий
# (одновременное получение одной и той же страницы разными пользователями; views будет увеличено только один раз)
# Класс F решает данную проблему
# Вычисления на стороне СУБД
# Django содержит набор функций Database Functions, которые позволяют делать вычисления на стороне СУБД
# Это и функции работы со строками, датой, математические функции и так далее.
# Эти функции рекомендуется применять на практике
# Рассмотрим работу функции Length() (вычисляет длину строки)
from django.db.models.functions import Length
# Аннотируем новое вычисляемое поле, например, для заголовков статей
ps = Women.objects.annotate(len=Length('title'))
ps  # <QuerySet [<Women: Анджелина Джоли>, ...]>
for item in ps:
     print(item.title, item.len)
# Анджелина Джоли 15 ...
# По аналогии используются и остальные функции
# raw SQL-запросы
# Непосредственно выполнить SQL-запрос можно через метод Manager.raw(<SQL-запрос>)
Women.objects.raw('SELECT * FROM women_women')  # <RawQuerySet: SELECT * FROM women_women>
w = _
for p in w:
     print(p.pk, p.title)
# 1 Анджелина Джоли ...
# Тот же результат получим и при использовании Category
w = Category.objects.raw('SELECT * FROM women_women')
w   # <RawQuerySet: SELECT * FROM women_women>
# Сами объекты w будут экземплярами класса Category
w[0]    # <Category: Актрисы>
# Нюансы метода raw()
# 1. "ленивое" исполнение запроса, то есть, отложенная загрузка информации до момента первого обращения к ней
from django.db import reset_queries
reset_queries() # функция для очистки connection.queries
connection.queries  # []
w = Women.objects.raw('SELECT * FROM women_women')
connection.queries  # [] (не было сгенерировано ни одного запроса)
w[0]    # <Women: Анджелина Джоли>
connection.queries  # [{'sql': 'SELECT * FROM women_women', 'time': '0.000'}]
# 2. При выборке конкретных полей в команде SELECT мы обязаны всегда указывать поле id
w = Women.objects.raw('SELECT id, title FROM women_women')
w   # <RawQuerySet: SELECT id, title FROM women_women>
w = Women.objects.raw('SELECT title FROM women_women')
w[0]    # django.core.exceptions.FieldDoesNotExist: Raw query must include the primary key
w = Women.objects.raw('SELECT id, title FROM women_women')
w[0].is_published   # True (хотя мы не указывали это поле в запросе)
connection.queries  # был выполнен дополнительный запрос (механизм отложенной загрузки полей)
# Это не лучшая практика (неоправданная нагрузка СУБД, особенно в цикле)
# Передача параметров в запрос
# Запрос на выбор записи по слагу
Women.objects.raw("SELECT id, title FROM women_women WHERE slug='shakira'")
# <RawQuerySet: SELECT id, title FROM women_women WHERE slug='shakira'>
# Обычно вместо значения слага используют параметр
slug = 'shakira'
Women.objects.raw("SELECT id, title FROM women_women WHERE slug='" + slug + "'")
# <RawQuerySet: SELECT id, title FROM women_women WHERE slug='shakira'>
# Это прямой путь к SQL-инъекциям
# Используем механизм параметров raw запросов (через список параметров) (безопасный путь)
Women.objects.raw("SELECT id, title FROM women_women WHERE slug='%s'", [slug])
# RawQuerySet: SELECT id, title FROM women_women WHERE slug='shakira'>
"""


# Create your models here.
# UPD on 17.08.2023 - Lesson 4
# Создаём класс Women (название м.б. произвольным), он соответствует таблице Women в базе данных
# Наследуем данный класс от базового класса Model, определяющего механизмы создания классов моделей
# Поле id уже присутствует в классе Model, его доопределять не нужно
# По умолчанию, последовательность полей в таблице будет такой же, как в модели
class Women(models.Model):
    """
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

    # UPD on 21.08.2023 - Lesson 9
    # Внешний ключ (будет называться cat_id)
    # Можно передавать модель не как строку, но тогда класс Category должен быть определён в коде ранее
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    # cat = models.ForeignKey(Category, on_delete=models.PROTECT)
    # Нужно осуществить миграцию
    # python manage.py makemigrations
    # Первоначально возникает ошибка, т.к. нет таблицы Category
    # 2 # выбираем вторую опцию
    # null=True - разрешаем установку NULL в существующие записи
    # python manage.py makemigrations
    # python manage.py migrate
    # В реальных проектах рекомендуется продумывать структуру БД заранее
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    """

    # UPD on 21.08.2023 - Lesson 10
    # Устанавливаем параметр verbose_name
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    # UPD on 21.08.2023 - Lesson 12
    # Добавляем в модель Women слаг
    # unique=True - слаг должен быть уникальным
    # Нужно внести изменения в БД
    # python manage.py makemigrations
    # Возникает предупреждение, что slug не может быть пустым
    # 2
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    # UPD on 22.08.2023 - Lesson 12
    # Нужно удалить все миграции, чтобы перестроить БД
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категории")
    # UPD on 23.08.2023 - Lesson 16
    # Можно переименовать свойство women_set на другое
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории", related_name='get_posts')

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
    # python manage.py migrate (помимо таблицы women_women будут созданы
    # и другие таблицы (для администрирования и т.д.))

    # UPD on 17.08.2023 - Lesson 5
    # Если в терминале выполнить команду
    # python manage.py shell
    # то откроется консоль фреймворка Django
    # В ней можно работать с командами ORM

    # UPD on 18.08.2023 - Lesson 5 (CRUD)
    # Последовательность выполнения команд в InteractiveConsole:
    # ---   CREATE  ---
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
    # Коллекция queries содержит список sql-запросов, которые были выполнены
    # Коллекция включает словари с двумя ключами: 'sql' (сам запрос) и 'time' (время выполнения)
    # w2 = Women(title='Энн Хэтэуэй', content='Биография Энн Хэтэуэй')  # добавим новую запись
    # w2.save()
    # connection.queries    # sql-запросов уже 2
    # w3 = Women()  # создаём запись, но данными заполняем не сразу
    # w3.title = 'Джулия Робертс'
    # w3.content = 'Биография Джулии Робертс'
    # w3.save()
    # Таким образом, благодаря ленивым запросам можно
    # наполнять записи данными в разном порядке, а только потом сохранять
    # Каждый класс модели содержит спец. статический объект objects
    # # objects
    # Этот объект берётся из базового класса модели и представляет собой ссылку на спец.класс manager
    # Women.objects # ссылка на объект класса manager (менеджер записей)
    # w4 = Women.objects.create(title='Ума Турман', content='Биография Умы Турман') # не создаём экземпляр класса
    # Отличие от предыдущего способа создания записей - запись сразу сохраняется в БД
    # w4    # <Women: Women object (4)>
    # w4.title
    # w4.pk
    # Можем создавать записи без использования переменной
    # Women.objects.create(title='Кира Найтли', content='Биография Киры Найтли')    # <Women: Women object (5)>
    #   --- READ    ---
    # Просмотр записей может быть осуществлён с помощью менеджера записей
    # Women.objects.all()   # выводит идентификаторы всех записей

    # UPD on 18.08.2023 - Lesson 5
    # Определяем метод, выводящий заголовки записей БД
    # self - ссылка на текущий экземпляр класса Women (т.е. на запись)
    def __str__(self):
        return self.title

    # UPD on 18.08.2023 - Lesson 5
    #   --- READ    ---
    # Чтобы изменения вступили в силу, нужно перезапустить оболочку
    # exit()
    # python manage.py shell
    # from women.models import Women
    # Women.objects.all()   # уже выводятся заголовки статей
    # Можно выбирать отдельные записи из списка
    # w = _
    # w[0]  # <Women: Анджелина Джоли>
    # w[1]  # <Women: Энн Хэтэуэй>
    # У записей можно выбирать отдельные поля
    # w[0].title
    # w[0].content
    # len(w)    # общее количество записей
    # Т.к. список - итерируемый объект, то можем перебрать его элементы - записи
    # for wi in w:
    #   print(wi.title)
    # В методе all() при выводе в консоль стоит ограничение на ~20 запись, но возвращает она все записи
    # Можно выбирать записи по условию (метод filter())
    # Women.objects.filter(title='Энн Хэтэуэй') # <QuerySet [<Women: Энн Хэтэуэй>]>
    # Посмотрим соответствующий sql-запрос
    # from django.db import connection
    # connection.queries
    # Метод filter() ~ WHERE
    # Women.objects.filter(title='Энн') # вернётся пустой список
    # Women.objects.filter(pk > 2)  # NameError: name 'pk' is not defined
    # pk - именованный атрибут
    # Women.objects.filter(pk=2)    # <QuerySet [<Women: Энн Хэтэуэй>]>
    # Для Women.objects.filter() существуют конструкции <имя атрибута>__gte ~ >=
    # и <имя атрибута>__lte ~ <=
    # Women.objects.filter(pk__gte=2)   # вернулись 4 записи
    # Women.objects.exclude(pk=2)   # exclude() - противоположность filter()
    # Если нужно выбрать запись по определённому условию, то можно использовать метод filter()
    # Women.objects.filter(pk=2)    # <Women: Энн Хэтэуэй>
    # НО рекомендуется использовать метод get()
    # Women.objects.get(pk=2)   # <Women: Энн Хэтэуэй>
    # Women.objects.get(pk__gte=2)  # raise self.model.MultipleObjectsReturned(...
    # Women.objects.get(pk=20)   # raise self.model.DoesNotExist(...
    # Метод get() позволяет убедиться, что в таблице только одна запись соответствует условию
    # Можно сортировать записи при выборке (метод order_by())
    # Women.objects.filter(pk__lte=4).order_by('title')
    # Можно вызывать методы цепочкой друг за другом (1 sql-запрос)
    # Women.objects.order_by('title')
    # Women.objects.order_by('-time_update')    # минус '-' - обратный порядок сортировки
    # Women.objects.order_by('time_update')
    #   --- UPDATE  ---
    # Обновление записи можно осуществить следующим образом
    # wu = Women.objects.get(pk=2)
    # wu.title = 'Марго Робби'
    # wu.content = 'Биография Марго Робби'
    # wu.save()
    # connection.queries
    #   --- DELETE  ---
    # Удаление записей можно осуществить следующим образом
    # wd = Women.objects.filter(pk__gte=4)
    # wd
    # wd.delete()   # delete - метод удаления (были удалены 2 записи)

    # UPD on 21.08.2023 - Lesson 8
    # Функция для динамического формирования url-адреса для конкретной записи
    # reverse берёт адрес из urls.py
    # Для самостоятельных ссылок на элементы сайта, не связанные с БД, лучше использовать тег url
    """
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})
    """

    # UPD on 22.08.2023 - Lesson 12
    # Формируем ссылку на основе слага
    # При этом мы не вносим изменений в шаблон, т.к. он формируется на основе get_absolute_url
    # Django автоматически защищает такие адреса от sql-инъекций
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # UPD on 21.08.2023 - Lesson 10
    # Если использовать не get_absolute_url, то в админ-панели не будет кнопки "Смотреть на сайте"
    """
    def get_absolute_url2(self):
        return reverse('post', kwargs={'post_id': self.pk})
    """

    # UPD on 21.08.2023 - Lesson 10
    # Пусть в админ-панели будет отображаться не Women, а Известные женщины
    # Создаём вложенный класс Meta (встроенный в Django)
    # Получается Известные женщиныs
    # Добавляем verbose_name_plural
    # Упорядочим статьи по времени создания и заголовку (ordering)
    # По умолчанию сортировка применяется и к записям из модели Women
    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        # '-' - сортировка в обратном порядке
        # ordering = ['time_create', 'title']
        # UPD on 23.08.2023 - Lesson 16
        # ИСПРАВЛЕНИЕ ОШИБКИ НАСЧЁТ ФУНКЦИИ annotate() ПО ПРИМЕРУ В УРОКЕ
        # ordering = ['-time_create', 'title']


# UPD on 21.08.2023 - Lesson 9
# Нужно добавить новую таблицу category в БД и связать с таблицей Women
# Фреймворк Django имеет три специальных класса для организации связей:
# ForeignKey – для связей Many to One (поля отношений);
# ManyToManyField – для связей Many to Many (многие ко многим);
# OneToOneField – для связей One to One (один к одному).
# Мы будем использовать ForeignKey
# ForeignKey(<ссылка на первичную модель>, on_delete=<ограничения при удалении записей из первичной модели>)
# В нашем случае category - первичная модель, women - вторичная
# В свою очередь, опция on_delete может принимать следующие значения:
# models.CASCADE – при удалении записи из первичной модели (у нас это таблица Category) происходит
# удаление всех записей из вторичной модели (Women), связанных с удаляемой категорией;
# models.PROTECT – запрещает удаление записи из первичной модели, если она
# используется во вторичной (выдает исключение);
# models.SET_NULL – при удалении записи первичной модели устанавливает значение
# foreign key в NULL у соответствующих записей вторичной модели;
# models.SET_DEFAULT – то же самое, что и SET_NULL, только вместо значения NULL
# устанавливает значение по умолчанию, которое должно быть определено через класс ForeignKey;
# models.SET() – то же самое, только устанавливает пользовательское значение;
# models.DO_NOTHING – удаление записи в первичной модели не вызывает никаких действий у вторичных моделей.


# UPD on 21.08.2023 - Lesson 9
# Создаём новый класс-модель Category
# Поле-id добавится автоматически
class Category(models.Model):
    # db_index=True - поле id будет проиндексировано (более быстрый поиск)
    # name = models.CharField(max_length=100, db_index=True)

    # UPD on 21.08.2023 - Lesson 10
    # Изменения с verbose_name желательно внести в БД с помощью миграций
    # python manage.py makemigrations
    # python manage.py migrate
    # Далее работаем с админ-панелью
    # Веб-сервер Django автоматически загружает фото в нужный каталог
    # Загрузим все фото
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    # UPD on 22.08.2023 - Lesson 12
    # python manage.py makemigrations
    # python manage.py migrate
    # Нужно удалить прежнюю версию БД, чтобы миграция применилась
    # python manage.py migrate
    # Нужно заново создать суперпользователя для админ-панели
    # python manage.py createsuperuser
    # root  # имя пользователя
    # root@coolsite.ru  # адрес эл.почты
    # Создание пароля
    # y
    # python manage.py runserver
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    # UPD on 21.08.2023 - Lesson 9
    # Добавляем функцию для формирования ссылок
    """
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})
    """

    # UPD on 22.08.2023 - Lesson 12
    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: ДОБАВИТЬ ИСПОЛЬЗОВАНИЕ СЛАГОВ В ОТОБРАЖЕНИЕ URL-АДРЕСОВ КАТЕГОРИЙ
    # UPD on 23.08.2023 - Lesson 15
    # ОШИБКИ NoReverseMatch at / НЕ ВОЗНИКАЕТ ИЗ-ЗА ТОГО, ЧТО ПЕРЕОПРЕДЕЛИЛА ФУНКЦИЮ В Lesson 12
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # UPD on 21.08.2023 - Lesson 10
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# UPD on 21.08.2023 - Lesson 9
# Добавим записи в таблицу category
# python manage.py shell
# from women.models import *
# Category.objects.create(name='Актрисы')
# Category.objects.create(name='Певицы')
# Заполним поле cat_id таблицы women
# w_list = Women.objects.all()
# w_list.update(cat_id=1)
# Классы моделей и их экземпляры
# Women.title   # ссылка на объект (без конкретной информации)
# w1 = Women(title='t1', content='c1', cat_id=1)  # title - строка, cat_id - ссылка на экземпляр класса Category
# Это всё делает конструктор класса Model
# type(w1.title)    # <class 'str'>
# w1.title  # 't1'
# type(w1.cat)  # <class 'women.models.Category'>
# w1.pk
# print(w1.id, w1.time_create, w1.time_update)  # None None None
# from django.db import connection
# connection.queries
# exit()
# Перезапустим консоль Django
# python manage.py shell
# from women.models import *
# w1 = Women(title='t1', content='c1', cat_id=1)
# from django.db import connection
# connection.queries    # []
# w1.cat    # <Category: Актрисы>
# connection.queries    # [{'sql': 'SELECT "women_category"."id", "women_category"."name" FROM "women_category"
# WHERE "women_category"."id" = 1 LIMIT 21', 'time': '0.000'}]
# Django обращается к БД только при необходимости
# w2 = Women.objects.get(pk=2)
# connection.queries
# w2.title
# w2.cat
# connection.queries
# w2.cat.name   # 'Актрисы'
# exit()
