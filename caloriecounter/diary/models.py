from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from caloriecounter.food.models import FoodProduct, Unit, FoodProductNutrient
from caloriecounter.user.models import User


class DiaryEntryManager(models.Manager):
    """
    Since we're often performing calculations on DiaryEntries (Nutritional information, etc.),
    this manager adds a prefetch for products, nutrients and units, to reduce overhead.
    """
    def get_queryset(self):
        return super().get_queryset()\
            .select_related('product',
                            'unit',
                            'product__default_unit')\
            .prefetch_related('product__foodproductnutrient_set',
                              'product__foodproductnutrient_set__nutrient')


class DiaryEntry(models.Model):
    class Meta:
        ordering = ['-date', 'time']
        verbose_name = _('diary entry')
        verbose_name_plural = ('diary entries')

    objects = DiaryEntryManager()

    user = models.ForeignKey(to=User, verbose_name=_('user'), on_delete=models.CASCADE, blank=False, editable=False)

    created_on = models.DateTimeField(verbose_name=_('created on'), auto_now_add=True)

    date = models.DateField(_("entry Date"), blank=False, default=datetime.now)
    time = models.TimeField(_("entry Time"), blank=False, default=datetime.now)

    product = models.ForeignKey(to=FoodProduct, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.FloatField(verbose_name=_('quantity'), validators=[MinValueValidator(0),])
    unit = models.ForeignKey(verbose_name=_('unit'), to=Unit, on_delete=models.SET_NULL, null=True, blank=True)

    # Return a list of tuples containing the unit, and the quantity of each Nutrient for this diary entry.
    @property
    def nutritional_information(self):
        try:
            self.product
        except FoodProduct.DoesNotExist:
            return []

        quantity = self.quantity
        list_of_nutrients = []
        if self.unit:
            try:
                quantity = self.product.get_quantity_in_default_unit(self.quantity, self.unit)
            except ValueError:
                quantity = 0
        else:
            quantity = self.quantity * self.product.default_quantity

        for product_nutrient in self.product.foodproductnutrient_set.all():
            if quantity == 0:
                list_of_nutrients.append((None, product_nutrient.nutrient))
            else:
                list_of_nutrients.append((quantity * (product_nutrient.quantity / 100), product_nutrient.nutrient))

        return list_of_nutrients

    def clean(self):
        super().clean()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        if exclude is None:
            exclude = []

        errors = {}

        # Check if the DiaryEntry's unit is valid for this product.
        if 'unit' not in exclude:
            try:
                self.product.get_quantity_in_default_unit(self.quantity, self.unit)

            except ValueError:
                errors['unit'] = ValidationError(_('Unknown unit "{unit}" for product "{product}"')
                                                 .format(unit = self.unit, product = self.product),
                                                 code='unit_does_not_match_product')
            pass

        if 'product' not in exclude:
            if not self.unit and self.product.default_quantity == 0:
                errors['product'] = ValidationError(
                    _('Cannot convert {quantity} {product} to {unit} of {product}').format(
                        quantity = self.quantity,
                        product= self.product,
                        unit = self.product.default_unit),
                    code='can_not_convert_quantity_of_product_to_unit')
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.unit:
            if self.product.default_quantity == 0:

                raise ValidationError(_('Cannot convert {quantity} {product} to {unit} of {product}')
                                      .format(quantity = self.quantity,
                                              product = self.product,
                                              unit = self.product.default_unit),
                                    code='can_not_convert_quantity_of_product_to_unit')

        super().save(*args, **kwargs)

    def __str__(self):
        if self.unit:
            string = '{date} at {time} - {quantity} {unit} of {product}'
        else:
            string = '{date} at {time} - {quantity} {product}'

        return string.format(quantity=self.quantity,
                             unit=self.unit,
                             product=self.product,
                             time=self.time,
                             date=self.date)
