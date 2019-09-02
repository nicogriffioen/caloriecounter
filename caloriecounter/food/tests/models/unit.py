from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.test import TestCase
from caloriecounter.food.models import Unit


class UnitTest(TestCase):
    # This is the TestCase class for the Unit model.
    #
    # Note: When testing with actual conversions, we avoid using numbers like 0 or 1,
    # because those have a high likelihood of being default numbers for certain fields.
    #
    # One thing to consider in the future is whether we want to move the validation errors to a generic function,
    # and whether we want to test the specific non_field_errors.

    @classmethod
    def setUpTestData(cls):
        parent = Unit(name='parent', short_name='p', is_base=True, is_constant=True)
        parent.save()
        parent_non_base = Unit(name='parent_non_base', short_name='p', is_base=False, is_constant=True)
        parent_non_base.save()
        ml = Unit(name="mililiter", short_name='ml', is_base=True, is_constant=True)
        ml.save()
        l = Unit(name="liter", short_name='l', is_base=False,
                 is_constant=True, parent=ml, base_unit_multiplier=1000)
        l.save()
        cup = Unit(name="cup", short_name='cup', is_base=False, is_constant=True,
                   parent=ml, base_unit_multiplier=136)
        cup.save()
        g = Unit(name="gram", short_name='g', is_base=True, is_constant=True)
        g.save()
        kg = Unit(name="kilogram", short_name='g', is_base=False, is_constant=True, parent=g, base_unit_multiplier=1000)
        kg.save()
        bowl = Unit(name="bowl", short_name='bowl', is_base=False, is_constant=False, base_unit_multiplier=2)
        bowl.save()

        # Assert:
    # 1. A unit is represented by it's name when converted to a string
    # 2. A unit is represented by it's correct plural_form
    def test_to_string(self):
        unit = Unit(name='gram')
        self.assertEqual(str(unit), unit.name)

        self.assertEqual(unit.name_plural, 'grams')

    def test_custom_name_plural(self):
        unit = Unit(name='ox', _name_plural='oxen')

        self.assertEqual(unit.name_plural, 'oxen')

    # Assert:
    # 1. All values are initialized correctly
    def test_assert_default_values(self):
        unit = Unit(name='gram', short_name='g')
        self.assertEqual(unit.name, 'gram')
        self.assertIsNone(unit._name_plural)
        self.assertFalse(unit.is_base)
        self.assertTrue(unit.is_constant)
        self.assertIsNone(unit.parent)
        self.assertEqual(unit.base_unit_multiplier, 1)


    # Assert:
    # 1. The base_unit property returns self for a base unit
    # 2. The base_unit property returns base for a child unit
    # 2. The base_unit property returns self for a unit with no parent.
    def test_base_unit(self):
        unit = Unit.objects.get(name='parent')
        self.assertEqual(unit, unit.base_unit)

        parent_unit = Unit.objects.get(name='gram')
        unit = Unit.objects.get(name='kilogram')
        self.assertEqual(parent_unit, unit.base_unit)

        unit = Unit.objects.get(name='bowl')
        self.assertEqual(unit, unit.base_unit)

    # Assert
    # 1. An error is raised when parent is set to a value, but is_base is set to True.
    # 2. No error is raised when parent is set to a value, and is_base is False
    def test_parent_is_base(self):
        parent_unit = Unit.objects.get(name='parent')
        unit = Unit(name='child', short_name='c', is_base=True, is_constant=True, parent=parent_unit)

        try:
            unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        unit.is_base = False
        unit.full_clean()


    #Assert:
    # 1. Validation error is raised when trying to set a unit's parent to a unit where is_base is False
    # 2. Validation error is raised when saving a parent where is_base is False
    # 3. No error is raised when setting a unit's parent to a unit where is_base is True
    # 4. No validation error is raised when saving a parent where is_base is True
    def test_parent_unit_parent_is_not_base(self):
        parent_unit = Unit.objects.get(name='parent_non_base')
        unit = Unit(name='child', short_name='c', is_base=True, is_constant=True, parent=parent_unit)

        try:
            unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        parent_unit = Unit.objects.get(name='parent')
        unit.parent = parent_unit
        unit.is_base = False

        unit.save()

        parent_unit.is_base = False

        try:
            parent_unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        parent_unit.is_base = True
        parent_unit.full_clean()

    # Assert:
    # 1. Saving a unit with is_constant False and is_base being True will raise a ValueError
    def test_not_is_constant_is_base(self):
        unit = Unit(name='unit', short_name='c', is_base=True, is_constant=False)

        try:
            unit.full_clean()
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertTrue(NON_FIELD_ERRORS in e.message_dict)

        unit.is_base = False

        unit.save()

    # Assert:
    # 1. convert_to_base returns the exact quantity for a base unit
    # 2. convert_to_base returns quantity * base_unit_multiplier for a child unit
    # 3. convert_to_base returns quantity for a non-base unit without a parent
    def test_convert_to_base(self):
        g = Unit.objects.get(name='gram')
        self.assertEqual(16, g.convert_to_base(16))

        kg = Unit.objects.get(name='kilogram')
        self.assertEqual(1600, kg.convert_to_base(1.6))

        bowl = Unit.objects.get(name='bowl')
        self.assertEqual(210, bowl.convert_to_base(210))

    # Assert:
    # 1. Converting a unit to itself returns the passed quantity for:
    #       - A base unit
    #       - A child unit
    #       - A non-base non-child unit
    # 2. Converting a base_unit to its child returns the correct value
    # 3. Converting a child unit to its parent returns the correct value
    # 4. Converting a child unit to another child returns the correct value
    # 5. Converting two unrelated child units raises a ValueError
    # 6. Converting a child unit to an unrelated non-child unit raises a ValueError
    # 7. Converting a base unit unit to an unrelated child unit raises a  ValueError
    # 8. Converting a base unit unit to an unrelated non-child unit raises a ValueError
    # 9. Converting a non-child unit to another unit raises a ValueError
    def test_convert_to_unit(self):
        ml = Unit.objects.get(name='mililiter')
        l = Unit.objects.get(name='liter')
        cup = Unit.objects.get(name='cup')
        g = Unit.objects.get(name='gram')
        kg = Unit.objects.get(name='kilogram')
        bowl = Unit.objects.get(name='bowl')

        # Assert 1.
        # Test on different units, to ensure it works for al
        self.assertEqual(16, g.convert_to_unit(16, g))
        self.assertEqual(19, kg.convert_to_unit(19, kg))
        self.assertEqual(18, cup.convert_to_unit(18, cup))

        # Assert 2.
        self.assertEqual(1.6, g.convert_to_unit(1600, kg))

        # Assert 3.
        self.assertEqual(2400, kg.convert_to_unit(2.4, g))

        # Assert 4.
        self.assertEqual(0.408, cup.convert_to_unit(3, l))

        # Assert 5.
        try:
            kg.convert_to_unit(23, cup)
            raise AssertionError("ValueError not raised")
        except ValueError as e:
            pass

        # Assert 6.
        try:
            kg.convert_to_unit(23, bowl)
            raise AssertionError("ValueError not raised")
        except ValueError as e:
            pass

        # Assert 7.
        try:
            g.convert_to_unit(23, cup)
            raise AssertionError("ValueError not raised")
        except ValueError as e:
            pass

        # Assert 8.
        try:
            kg.convert_to_unit(23, bowl)
            raise AssertionError("ValueError not raised")
        except ValueError as e:
            pass

        # Assert 9.
        try:
            bowl.convert_to_unit(23, kg)
            raise AssertionError("ValueError not raised")
        except ValueError as e:
            pass