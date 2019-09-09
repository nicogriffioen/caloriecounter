from django.test import TestCase


class AppConfigTest(TestCase):
    def test_config(self):
        from .apps import UserConfig
