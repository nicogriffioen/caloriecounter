from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from django.utils.translation import ugettext as _

from caloriecounter.diary.models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = ['pk', 'date', 'time', 'product', 'quantity', 'unit', 'nutritional_information']

    nutritional_information = SerializerMethodField()

    def validate(self, data):
        errors = {}
        if self.partial:
            product = data.get('product', self.instance.product)
            unit = data.get('unit', self.instance.unit)
            quantity = data.get('quantity', self.instance.quantity)
        else:
            product = data.get('product', None)
            unit = data.get('unit', None)
            quantity = data.get('quantity', None)

        try:
            product.get_quantity_in_default_unit(quantity, unit)
        except ValueError:
            errors['unit'] = ValidationError(_('Unknown unit "{unit}" for product "{product}"')
                                             .format(unit = unit, product = product),
                                             code='unit_does_not_match_product')

        if not 'unit' in data and product.default_quantity == 0:
            errors['product'] = ValidationError(
                _('Cannot convert {quantity} {product} to {unit} of {product}').format(
                    quantity = quantity,
                    product= product,
                    unit = product.default_unit),
                code='can_not_convert_quantity_of_product_to_unit')

        if errors:
            raise ValidationError(errors)
        return data

    def get_nutritional_information(self, obj : DiaryEntry):
        list = []
        for (quantiy, nutrient) in obj.nutritional_information:
            list.append({
                'quantity' : quantiy,
                'nutrient' : nutrient.pk
            })

        return list