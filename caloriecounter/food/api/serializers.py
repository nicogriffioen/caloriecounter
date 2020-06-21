from rest_framework import serializers

from caloriecounter.food.models import FoodProduct, FoodGroup, Unit, Nutrient, FoodProductNutrient, FoodProductUnit, \
    FoodProductCommonName


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


class NutritionalInformationSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    quantity = serializers.FloatField()
    nutrient = NutrientSerializer()


class FoodProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProductUnit
        fields = ['pk', 'unit', 'multiplier', 'description', 'modifier']


class FoodProductCommonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProductCommonName
        fields = ('id', 'text', 'text_plural')


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ['pk', 'full_name', 'common_name', 'food_source', 'default_unit', 'default_quantity', 'food_group',
                  'nutritional_information', 'units', 'common_names']

    def get_common_name(self, instance) -> FoodProductCommonName:
        if hasattr(instance, 'common_name') and instance.common_name is not None:
            common_name = next((x for x in instance.common_names.all() if x.pk == instance.common_name), None)
            if common_name:
                return FoodProductCommonNameSerializer(common_name).data

        return None

    common_names = FoodProductCommonNameSerializer(many=True)
    common_name = serializers.SerializerMethodField('get_common_name')
    nutritional_information = NutritionalInformationSerializer(source='foodproductnutrient_set', many=True)
    units = FoodProductUnitSerializer(source='foodproductunit_set', many=True)
