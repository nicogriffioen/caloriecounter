from django.apps import AppConfig
from .signals import pre_save_handler


class FoodConfig(AppConfig):
    name = 'food'
