import datetime

from caloriecounter.diary.models import DiaryEntry
from caloriecounter.food.tests import BaseTest, ValidationError, TestCase
from caloriecounter.user.models import User


class AppConfigTest(TestCase):

    def test_app_config(self):
        from caloriecounter.diary.apps import DiaryConfig
        self.assertEquals(DiaryConfig.name, 'diary')


class DiaryEntryTest(BaseTest):

    def setUp(self):
        super().setUp()

        self.user = User.objects.create_user('calorieuser', 'test@calorie-counter.test', 'password123')
        self.user.save()

        self.diary_entry = DiaryEntry.objects.create(user = self.user,
                                                     product=self.product,
                                                     date=datetime.date(2018, 3, 3),
                                                     time=datetime.time(hour=21, minute=20),
                                                     quantity=20,
                                                     unit=self.g)
        self.diary_entry.save()

    def test_string(self):
        self.assertEqual(str(self.diary_entry), '2018-03-03 at 21:20:00 - {0} {1} of {2}'.format(20, self.g, self.product))

        self.diary_entry.unit = None
        self.assertEqual(str(self.diary_entry),
                         '2018-03-03 at 21:20:00 - {0} {1}'.format(20, self.product.display_name))
        pass

    # Assert that a ValidationError is raised for a unit that can not be converted to the product's default unit.
    def test_product_quantity_unit_match(self):
        with self.assertRaises(ValidationError) as raises_ve:
            entry = DiaryEntry.objects.create(user=self.user,
                                              product=self.product,
                                              date=datetime.date(year=2018, month=3, day=3),
                                              time=datetime.time(hour=21, minute=20),
                                              quantity=3,
                                              unit=self.handful)

            entry.full_clean()
            entry.unit=self.bowl
            entry.full_clean()

    # Assert that a validation error is raised when adding DiaryEntry that has a negative quantity.
    def test_product_min_quantity(self):
        with self.assertRaises(ValidationError) as raises_ve:
            entry = DiaryEntry.objects.create(user=self.user,
                                              product=self.product,
                                              date=datetime.date(year=2018, month=3, day=3),
                                              time=datetime.time(hour=21, minute=20),
                                              quantity=-3,
                                              unit=self.g)

            entry.full_clean()
            entry.save()

    # Assert that a product's default quantity is used
    # when adding a DiaryEntry with only quantity and product
    def test_no_unit(self):
        entry = DiaryEntry.objects.create(user=self.user,
                                          product=self.product,
                                          date=datetime.date(year=2018, month=3, day=3),
                                          time=datetime.time(hour=21, minute=20),
                                          quantity=54)
        entry.save()

        self.assertIsNone(entry.unit)
        self.assertEquals(54, entry.quantity)

    # Assert that a ValidationError is raised on the unit field
    # when adding a DiaryEntry with only quantity and product,
    # where the product has no default_quantity.
    def test_no_unit_no_default_quantity(self):
        with self.assertRaises(ValidationError) as raises_ve:
            entry = DiaryEntry.objects.create(user=self.user,
                                          product=self.product_no_default_quantity,
                                          date=datetime.date(year=2018, month=3, day=3),
                                          time=datetime.time(hour=21, minute=20),
                                          quantity=20)

        entry = DiaryEntry(user=self.user,
                           product=self.product_no_default_quantity,
                           date=datetime.date(year=2018, month=3, day=3),
                           time=datetime.time(hour=21, minute=20),
                           quantity=20)

        with self.assertRaises(ValidationError) as raises_ve:
            entry.full_clean()

        entry.product = self.product
        entry.full_clean()
        entry.save()

    # Assert:
    # 1. Getting the nutritional information for a DiaryEntry contains the right number of results.
    # 2. The nutritional information is correct for the product's base_unit.
    # 3. The nutritional information is correct for a child unit.
    def test_product_nutritional_information(self):
        # Assert 1.
        self.assertEqual(len(self.diary_entry.nutritional_information), 2)

        # Assert 2.
        self.assertEqual(self.diary_entry.nutritional_information[0][0], 0.8)

        # Assert 3.
        self.diary_entry.unit = self.kg
        self.diary_entry.save()
        self.assertEqual(self.diary_entry.nutritional_information[0][0], 800)

    # Assert:
    # 1. Getting the nutritional information for a DiaryEntry without a unit contains the right number of results.
    # 2. The nutritional information is correct.
    def test_product_nutritional_information_no_unit(self):
        entry = DiaryEntry(user=self.user,
                            product=self.product,
                            date=datetime.date(year=2018, month=3, day=3),
                            time=datetime.time(hour=21, minute=20),
                            quantity=20)

        # Assert 1.
        self.assertEqual(len(entry.nutritional_information), 2)

        # Assert 2.
        self.assertEqual(entry.nutritional_information[0][0], 12)

    # Assert:
    # 1. Getting the nutritional information for a DiaryEntry without a unit,
    # without a default quantity contains the right number of results.
    #
    # 2. There are no quantities defined for each nutrition.
    def test_product_nutritional_information_no_unit_no_default_quantity(self):
        entry = DiaryEntry(user=self.user,
                           product=self.product_no_default_quantity,
                           date=datetime.date(year=2018, month=3, day=3),
                           time=datetime.time(hour=21, minute=20),
                           quantity=10)

        # Assert 1.
        self.assertEqual(len(entry.nutritional_information), 2)

        # Assert 2.
        self.assertEqual(entry.nutritional_information[0][0], None)

    # Assert:
    # 1. Getting the nutritional information for a DiaryEntry with an incompatible unit,
    # contains the right number of results.
    # 2. There are no quantities defined for each nutrition.
    def test_product_nutritional_information_incompatible_unit(self):
        entry = DiaryEntry.objects.create(user=self.user,
                                          product=self.product,
                                          date=datetime.date(year=2018, month=3, day=3),
                                          time=datetime.time(hour=21, minute=20),
                                          quantity=54,
                                          unit=self.handful)

        # Assert 1.
        self.assertEqual(len(entry.nutritional_information), 2)

        # Assert 2.
        self.assertEqual(entry.nutritional_information[0][0], None)

    # Assert:
    # 1. Getting the nutritional information for a DiaryEntry without a product returns an empty list.
    def test_product_nutritional_information_no_product(self):
        entry = DiaryEntry(user=self.user,
                           date=datetime.date(year=2018, month=3, day=3),
                           time=datetime.time(hour=21, minute=20),
                           quantity=54,
                           unit=self.handful)

        # Assert 1.
        self.assertEqual(len(entry.nutritional_information), 0)

