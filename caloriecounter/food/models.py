from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _


# Units like g, ml etc.
class Unit(models.Model):
    class Meta:
        ordering = ['-is_base', '-is_constant', 'base_unit_multiplier']
    name = models.TextField(verbose_name=_('name'), help_text=_('i.e. gram'), unique=True)
    _name_plural = models.TextField(verbose_name=_('plural name'),
                                    help_text=_('i.e. grams. Leave empty to use a programmatically set plural'),
                                    null=True, blank=True)

    short_name = models.TextField(verbose_name=_('Short name'), help_text=_('i.e. g'), null=False, blank=False)

    is_base = models.BooleanField(verbose_name=_('base unit'),
                                  help_text=_("""Determines whether a unit is a base unit. 
                                  Base units are units for which all nutrients for a product are defined.
                                  For instance Bread contains 200 kcal per 100 base units. 
                                  In this case, base unit is grams.
                                  Try to avoid defining multiple base units for one quantity."""),
                                  default=False)

    is_constant = models.BooleanField(verbose_name=_('constant'),
                                      help_text=_("""Determines whether a unit is constant. 
                                                    100 ml is the same for every product, 1 portion is not."""),
                                      default=True)

    parent = models.ForeignKey(verbose_name=_('parent unit'),
                               to='self',
                               limit_choices_to={'is_base': True},
                               on_delete=models.SET_NULL,
                               related_name='children',
                               null=True, blank=True)

    base_unit_multiplier = models.FloatField(verbose_name=_('multiplier'),
                                             help_text=_("""The multiplier to convert this unit to it's parent
                                                            To compare, 1 cup is 236 ml, so for the unit 'cup', 
                                                            the base unit multiplier will be 236"""),
                                             validators=[MinValueValidator(0), ],
                                             blank=True, default=1)

    def convert_to_base(self, quantity):
        if self.is_base or not self.parent:
            return quantity

        return self.base_unit_multiplier * quantity

    def convert_to_unit(self, quantity, unit):
        if unit == self:
            return quantity

        if unit == self.parent:
            return quantity * self.base_unit_multiplier

        if self == unit.parent:
            return quantity / unit.base_unit_multiplier

        if self.parent == unit.parent and self.parent is not None:
            return (quantity * self.base_unit_multiplier) / unit.base_unit_multiplier

        raise ValueError('Tried to convert two unrelated units.')

    @property
    def base_unit(self):
        if self.is_base:
            return self
        elif self.parent:
            return self.parent

        return self

    @property
    def name_plural(self):
        if self._name_plural is None:
            return _('{name}s').format(name=self.name)

        return self._name_plural

    def clean(self, *args, **kwargs):
        errors = []
        if self.is_base and self.parent:
            errors.append(ValidationError(_('Unit can not both be a base unit and have a parent defined.'), code='unit_both_base_and_child'))

        if not self.is_constant and self.is_base:
            errors.append(ValidationError(_('Base units must be constant.'), code='base_unit_not_constant'))
            pass

        if not self.is_base and not self.children.count() == 0:
            errors.append(ValidationError(_('Parent units must be base units.'), code='parent_unit_not_base'))

        if len(errors) > 0:
            raise ValidationError({
                NON_FIELD_ERRORS: errors,
            })

        super(Unit, self).clean(*args, **kwargs)

    def __str__(self):
        return self.name


# Foodgroups like Dairy, Poultry etc.
class FoodGroup(models.Model):
    name = models.TextField(verbose_name=_('name'), blank=False)

    def __str__(self):
        return self.name


# Foodproducts like broccoli, butter, etc.
class FoodProduct(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['full_name']),
        ]

        ordering=['full_name']

    full_name = models.TextField(verbose_name=_('full name'), null=False, blank=False)
    display_name = models.TextField(verbose_name=_('display name'), null=False, blank=False)

    food_source = models.TextField(null=True, blank=True)

    default_unit = models.ForeignKey(verbose_name=_('default unit'),
                                     to=Unit,
                                     limit_choices_to={'is_base': True},
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='default_products')

    default_quantity = models.FloatField(verbose_name=_('default quantity'),
                                         help_text=_('Determines the quantity in base units of 1 product.'),
                                         validators=[MinValueValidator(0), ])

    food_group = models.ForeignKey(verbose_name=_('food group'),
                                   to=FoodGroup, related_name='food_products', on_delete=models.SET_NULL, null=True)

    nutrients = models.ManyToManyField(verbose_name=_('nutrients'),
                                       to='Nutrient',
                                       through='FoodProductNutrient',
                                       related_name='products')

    units = models.ManyToManyField(verbose_name=_('units'), to=Unit, through='FoodProductUnit', related_name='products')

    # Converts a quantity of a random unit to a quantity of the default unit, if possible.
    def get_quantity_in_default_unit(self, quantity, unit: Unit = None):
        # 1. Unit is None:
        if unit is None:
            return quantity * self.default_quantity

        # 2. Current unit is explicitly defined in the food_product_unit
        food_product_unit = FoodProductUnit.objects.filter(product=self, unit=unit).first()

        if food_product_unit is not None:
            return food_product_unit.multiplier * quantity

        # 3. Current unit is either the product's default unit or a child of the product's unit
        if unit.base_unit == self.default_unit:
            return unit.convert_to_base(quantity)

        # 4. food_product_unit has a unit that is either the parent or a unit with a shared parent to current unit.
        food_product_unit = FoodProductUnit.objects.filter(product=self, unit__is_constant=True)\
            .filter(Q(unit__parent=unit.base_unit) | Q(unit = unit.base_unit))\
            .first()

        if food_product_unit is not None:
            return ((unit.base_unit_multiplier * quantity) / food_product_unit.unit.base_unit_multiplier) \
                   * food_product_unit.multiplier

        raise ValueError('Unit "{0}" is not a valid unit for product "{1}"'.format(unit, self))

    def __str__(self):
        if self.display_name and not self.display_name == '':
            return self.display_name
        else:
            return self.full_name


# Nutrients like Energy, Protein etc.
class Nutrient(models.Model):
    class Meta:
        ordering = ['-rank']
        pass

    name = models.TextField(verbose_name=_('name'), null=False, blank=False, unique=True)

    unit = models.ForeignKey(verbose_name=_('unit'), to=Unit, on_delete=models.SET_NULL, null=True)

    rank = models.IntegerField(verbose_name=_('rank'), default=-1)

    def __str__(self):
        return '{0} of {1}'.format(self.unit, self.name)


# Through model for nutrients per food product, containing the quantity.
class FoodProductNutrient(models.Model):
    class Meta:
        unique_together = [('product', 'nutrient'),]
        ordering = ['-nutrient__rank']
        indexes = [
            models.Index(fields=['product', 'nutrient']),
        ]
        pass

    product = models.ForeignKey(verbose_name=_('product'), to=FoodProduct, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(verbose_name=('nutrient'), to=Nutrient, on_delete=models.CASCADE)

    quantity = models.FloatField(verbose_name=_('quantity'), validators=[MinValueValidator(0), ])

    def __str__(self):
        return '{0} {1} per 100 {2} of {3}'.format(self.quantity, self.nutrient, self.product.default_unit,
                                                   self.product)


# Through model for nutrients per food product, containing the quantity,
class FoodProductUnit(models.Model):
    class Meta:
        unique_together = [('product', 'unit'),]

    product = models.ForeignKey(verbose_name=_('product'), to=FoodProduct, on_delete=models.CASCADE)

    unit = models.ForeignKey(verbose_name=_('name of the unit'),
                             to=Unit,
                             on_delete=models.SET_NULL,
                             null=True, blank=True)

    multiplier = models.FloatField(verbose_name=_('multiplier'),
                                   help_text=_("""Determines the base unit quantity of 1 of this unit, 
                                   i.e. 1 'glass' of milk is <multiplier> grams"""),
                                   validators=[MinValueValidator(0), ])

    def __str__(self):
        return '{0} of {1} ({2} {3})'.format(self.unit, self.product, self.multiplier, self.product.default_unit)

    def clean(self, *args, **kwargs):
        errors = []

        # Check if we can find an existing link between this unit, and the product's default unit
        if self.unit.is_constant:
            try:
                actual_conversion = self.unit.convert_to_unit(1, self.product.default_unit)
                errors.append(ValidationError(_("""1 %(unit)s is already defined as %(quantity)s %(unit2)s. 
                                                You can only specify conversions 
                                                of units that do not relate to each other, 
                                                like grams and milliliters."""),
                                              code='unit_already_defined_for_product',
                                              params= {
                                                  'unit' : self.unit,
                                                  'quantity' : actual_conversion,
                                                  'unit2' : self.product.default_unit
                                              }))
            except ValueError:
                pass

            try:
                actual_conversion = self.product.get_quantity_in_default_unit(1, self.unit)
                errors.append(ValidationError(_("""1 %(unit)s is already implicitly defined as %(quantity)s %(unit2)s. 
                                                There is already a related unit defined on this product."""),
                                              code='unit_already_implicitly_defined_for_product',
                                              params= {
                                                  'unit' : self.unit,
                                                  'quantity' : actual_conversion,
                                                  'unit2' : self.product.default_unit
                                              }))
            except ValueError:
                pass

        if len(errors) > 0:
            raise ValidationError({
                NON_FIELD_ERRORS: errors,
            })

        super(FoodProductUnit, self).clean(*args, **kwargs)
