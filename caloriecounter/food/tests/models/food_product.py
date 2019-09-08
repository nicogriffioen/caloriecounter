from django.contrib.admin import AdminSite
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.test import TestCase

from caloriecounter.food.models import FoodProduct, Unit, Nutrient, FoodGroup, FoodProductUnit, FoodProductNutrient
from caloriecounter.food.admin import FoodProductAdmin


class BaseTest(TestCase):

    # Set up the test data. This is a pretty beefy method, for a good reason.
    # Realistic test data is pretty explicit and interlinked, and it's a hassle to re-initialize it for every test,
    # so it's better to do it properly one time.
    # In the future, it's probably best to update this initialization code first.

    def setUp(self):

        #Set up units
        self.ml = Unit(name="mililiter", short_name='ml', is_base=True, is_constant=True)
        self.ml.save()
        self.l = Unit(name="liter", short_name='l', is_base=False,
                 is_constant=True, parent=self.ml, base_unit_multiplier=1000)
        self.l.save()
        self.cup = Unit(name="cup", short_name='cup', is_base=False, is_constant=True,
                        parent=self.ml, base_unit_multiplier=75)
        self.cup.save()
        self.g = Unit(name="gram", short_name='g', is_base=True, is_constant=True)
        self.g.save()
        self.kg = Unit(name="kilogram", short_name='g', is_base=False, is_constant=True, parent=self.g,
                       base_unit_multiplier=1000)
        self.kg.save()
        self.bowl = Unit(name="bowl", short_name='bowl',parent=self.ml ,is_base=False, is_constant=False,
                         base_unit_multiplier=1)
        self.bowl.save()
        self.handful = Unit(name="handful", short_name='handful', is_base=False, is_constant=False,
                            base_unit_multiplier=1)
        self.handful.save()

        # Set up nutrients
        self.fat = Nutrient(name='fat', unit=self.g)
        self.fat.save()
        self.protein = Nutrient(name='protein', unit=self.g)
        self.protein.save()

        # Set up food groups
        self.food_group = FoodGroup(name='Vegetables')
        self.food_group.save()

        # Set up products
        self.product = FoodProduct(full_name='Mushrooms (white,raw)',
                                   display_name='White mushrooms',
                                   default_quantity=15,
                                   default_unit=self.g,
                                   food_group=self.food_group)
        self.product.save()

        self.product_no_display_name = FoodProduct(full_name='Mushrooms (portobello,raw)',
                                                   display_name='Portobello mushrooms',
                                                   default_quantity=15,
                                                   default_unit=self.g,
                                                   food_group=self.food_group)
        self.product_no_display_name.save()

        self.product_no_default_quantity = FoodProduct(full_name='Mushrooms (portobello,cooked)',
                                                       display_name='Portobello mushrooms',
                                                       default_quantity=0,
                                                       default_unit=self.g,
                                                       food_group=self.food_group)
        self.product_no_default_quantity.save()

        self.product_no_display_name.save()

        self.food_product_nutrient_fat = FoodProductNutrient(product=self.product, nutrient=self.fat, quantity=4)
        self.food_product_nutrient_fat.save()

        self.food_product_nutrient_protein = FoodProductNutrient(product=self.product, nutrient=self.protein,
                                                                 quantity=6)
        self.food_product_nutrient_protein.save()

        self.food_product_nutrient_no_default_quantity_fat = FoodProductNutrient(
            product=self.product_no_default_quantity,
            nutrient=self.fat,
            quantity=8)
        self.food_product_nutrient_no_default_quantity_fat.save()

        self.food_product_nutrient_no_default_quantity_protein = FoodProductNutrient(
            product=self.product_no_default_quantity,
            nutrient=self.protein,
            quantity=12)
        self.food_product_nutrient_no_default_quantity_protein.save()

        self.food_product_unit_bowl = FoodProductUnit(product=self.product, unit=self.bowl, multiplier=200)
        self.food_product_unit_bowl.save()
        self.food_product_unit_ml = FoodProductUnit(product=self.product, unit=self.ml, multiplier=2)
        self.food_product_unit_ml.save()

        # Create a FoodProduct where a non-base unit is specified (in this case cups instead of mL)
        self.product_with_cup = FoodProduct(full_name='Mushrooms (shiitake,raw)',
                                            display_name='Shiitake mushrooms',
                                            default_quantity=20,
                                            default_unit=self.g,
                                            food_group=self.food_group)
        self.product_with_cup.save()
        self.food_product_unit_cup = FoodProductUnit(product=self.product_with_cup, unit=self.cup, multiplier=150)
        self.food_product_unit_cup.save()


class FoodProductTest(BaseTest):

    def test_food_group_to_string(self):
        self.assertEqual('Vegetables', str(self.food_group))

    def test_to_string(self):
        self.assertEqual(str(self.product), 'White mushrooms')

        self.product_no_display_name.display_name = ''
        self.assertEqual(str(self.product_no_display_name), 'Mushrooms (portobello,raw)')


    # Assert:
    # 1. get_quantity_in_default_unit returns the correct value for an explicitly defined unit.
    # 2. It returns the correct value for the default unit.
    # 3. It returns the correct value for a  child of the default unit.
    # 4. It returns the correct value for a food_product_unit has a unit with a shared parent to current unit.
    # 5. It returns the correct value for a food_product_unit that contains the parent unit to the current unit.
    #    There are two conversions with parent ml for parent_with_cup (cup & bowl), but only cup is defined constant.
    #    This is the one to be used.
    # 6. It raises a ValueError for a unit for which no conversion exists.
    # 7. It returns the correct value for no unit.
    def test_get_quantity_in_default_unit(self):
        # Assert 1.
        self.assertEqual(self.product.get_quantity_in_default_unit(3.5, self.bowl, ), 700)

        # Assert 2.
        self.assertEqual(self.product.get_quantity_in_default_unit(34, self.g), 34)

        # Assert 3.
        self.assertEqual(self.product.get_quantity_in_default_unit(2.45, self.kg), 2450)

        # Assert 4.
        self.assertEqual(self.product_with_cup.get_quantity_in_default_unit(0.3, self.l), 600)

        # Assert 5.
        self.assertEqual(self.product.get_quantity_in_default_unit(0.3, self.l), 600)

        # Assert 6.
        with self.assertRaises(ValueError) as raises_ve:
            self.product.get_quantity_in_default_unit(4, self.handful)

        # Assert 7.
        self.assertEqual(self.product.get_quantity_in_default_unit(9), 135)


class FoodProductNutrientTest(BaseTest):

    def test_nutrient_to_string(self):
        self.assertEqual(str(self.fat), 'gram of fat')

    def test_food_product_nutrient_to_string(self):
        self.assertEqual(str(self.food_product_nutrient_fat), '4.0 gram of fat per 100 gram of White mushrooms')

    def test_foodproduct_admin_get_nutrients(self):

        admin = FoodProductAdmin(FoodProduct, AdminSite())
        self.assertEqual(admin.get_nutrients(self.product), '4.0 gram of fat\n6.0 gram of protein')


class FoodProductUnitTest(BaseTest):

    def test_food_product_unit_to_string(self):
        self.assertEquals(str(self.food_product_unit_ml), 'mililiter of White mushrooms (2.0 gram)')

    # Assert:
    # 1. We can create custom unit with a shared parent to the product's already defined unit's,
    # so long as it is not constant.
    # 2. When a custom unit is defined for a product, but it is a child of the product's default unit,
    # a ValidationError is raised
    # 3. When a custom unit is defined for a product, but it's a parent of an already defined unit,
    # a ValidationError is raised.
    # 4. When a custom unit is defined for a product, but it has already been defined, a ValidationError is raised.
    # 5. When a custom unit is defined for a product,
    # but it shares its parent with an already defined unit for this product, a ValidationError is raised.
    def test_food_unit_duplicate_base_unit(self):

        # Assert 1.
        food_product_unit_1 = FoodProductUnit(product=self.product_with_cup, unit=self.bowl, multiplier=2)
        food_product_unit_1.save()

        # Assert 2.
        food_product_unit = FoodProductUnit(product=self.product_with_cup, unit=self.kg, multiplier=2)
        try:
            food_product_unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        # Assert 3.
        food_product_unit = FoodProductUnit(product=self.product_with_cup, unit=self.ml, multiplier=2)
        try:
            food_product_unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        # Assert 4.
        food_product_unit = FoodProductUnit(product=self.product_with_cup, unit=self.cup, multiplier=2)
        try:
            food_product_unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        # Assert 5.
        food_product_unit = FoodProductUnit(product=self.product_with_cup, unit=self.l, multiplier=2)
        try:
            food_product_unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        # Assert 6.
        food_product_unit = FoodProductUnit(product=self.product_with_cup, unit=self.handful, multiplier=2)
        food_product_unit.full_clean()