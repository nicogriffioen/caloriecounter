from django.test import TestCase


# This class tests all base functionality for this app.
# It loads any code not covered by other tests, to ensure that at least all code loads without issues
class AppConfigTest(TestCase):

    def test_app_config(self):
        from caloriecounter.food.apps import AppConfig

