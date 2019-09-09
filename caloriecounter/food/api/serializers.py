from rest_framework import serializers

from caloriecounter.food.models import FoodProduct, FoodGroup, Unit, Nutrient, FoodProductNutrient


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['pk', 'name', 'name_plural', 'short_name', 'is_base', 'is_constant', 'parent', 'base_unit_multiplier']


class FoodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodGroup
        fields = ['pk', 'name']


class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['pk', 'name', 'unit', 'rank']


class FoodProductNutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProductNutrient
        fields = ['quantity', 'nutrient']


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ['pk', 'full_name', 'display_name', 'food_source', 'default_unit', 'default_quantity', 'food_group', 'nutrients', 'units']

    nutrients = FoodProductNutrientSerializer(source='foodproductnutrient_set', many=True)