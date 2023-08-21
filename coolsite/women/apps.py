from django.apps import AppConfig


class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'

    # UPD on 21.08.2023 - Lesson 10
    # Пусть в заголовке админ-панели вместо Women будет Женщины мира
    verbose_name = 'Женщины мира'

    # UPD on 21.08.2023 - Lesson 10
    # МОЯ ПОПЫТКА НЕ ОТОБРАЖАТЬ Женщины мира
    # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.default
    default = False
