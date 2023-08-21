# UPD on 17.08.2023 - Lesson 4
# Модуль models содержит базовые классы моделей, на основе которых можно создавать свои модели БД
from django.db import models
from django.urls import reverse


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
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    # UPD on 21.08.2023 - Lesson 12
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категории")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

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
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    # UPD on 21.08.2023 - Lesson 10
    # Если использовать не get_absolute_url, то в админ-панели не будет кнопки "Смотреть на сайте"
    ''''
    def get_absolute_url2(self):
        return reverse('post', kwargs={'post_id': self.pk})
    '''

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
        ordering = ['-time_create', 'title']


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

    def __str__(self):
        return self.name

    # UPD on 21.08.2023 - Lesson 9
    # Добавляем функцию для формирования ссылок
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

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
