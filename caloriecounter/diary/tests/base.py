from unittest import TestCase


class AppConfigTest(TestCase):

    def test_app_config(self):
        from caloriecounter.diary.apps import DiaryConfig
        self.assertEquals(DiaryConfig.name, 'diary')