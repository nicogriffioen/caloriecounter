from django.contrib import admin

from .models import *


class NutrientAdmin(admin.ModelAdmin):
    search_fields = ['name']


class FoodGroupAdmin(admin.ModelAdmin):
    search_fields = ['name']


class FoodProductUnitAdmin(admin.ModelAdmin):
    list_filter = ['unit']
    search_fields = ['unit']
    autocomplete_fields = ['unit', 'product']


class FoodProductNutrientInlineAdmin(admin.TabularInline):
    model = FoodProductNutrient
    autocomplete_fields = ['nutrient', 'product']


class FoodProductUnitInlineAdmin(admin.TabularInline):
    model = FoodProductUnit
    autocomplete_fields = ['unit', 'product']


class FoodProductSynonymInlineAdmin(admin.TabularInline):
    model = FoodProductCommonName


class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name', 'short_name']
    list_display = ('name', 'base_unit_multiplier', 'parent', )
    list_filter = ('is_constant',)

    inlines = [FoodProductUnitInlineAdmin]


class FoodProductAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'food_source', 'food_group', 'default_unit')
    list_filter = ('food_source', 'food_group')
    search_fields = ('full_name',)
    inlines = (FoodProductUnitInlineAdmin, FoodProductNutrientInlineAdmin, FoodProductSynonymInlineAdmin)

    list_select_related = ('food_group', 'default_unit')

    def get_nutrients(self, obj):
        nutrients = [str(food_product_nutrient.quantity) + ' ' + str(food_product_nutrient.nutrient) for food_product_nutrient in FoodProductNutrient.objects.filter(product=obj)]

        return '\n'.join(nutrients)

    get_nutrients.short_description = 'Nutrients (per 100)'


class FoodProductSynonymAdmin(admin.ModelAdmin):
    search_fields = ['text']
    list_display = ['text', 'food_product']
    ordering = ['text']
    autocomplete_fields = ['food_product',]


admin.site.register(Unit, UnitAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(FoodGroup, FoodGroupAdmin)
admin.site.register(FoodProduct, FoodProductAdmin)
admin.site.register(FoodProductCommonName, FoodProductSynonymAdmin)
admin.site.register(FoodProductUnit, FoodProductUnitAdmin)
