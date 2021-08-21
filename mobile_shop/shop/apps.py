from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'


class SmartwatchConfig(AppConfig):
    name = "Smartwatch"
    verbose_name = "Smartwatches"


class HeadphonesConfig(AppConfig):
    name = "Headphones"
    verbose_name = "Headphones"


class EarbudsConfig(AppConfig):
    name = "Earbuds"
    verbose_name = "Earbuds"