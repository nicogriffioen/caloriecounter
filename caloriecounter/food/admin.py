from django.contrib import admin

from .models import *

#class TeachSubjectInline(admin.TabularInline):
#    model = TeachSubject
#    extra = 2 # how many rows to show


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_unit_multiplier', 'parent', )


class NutrientAdmin(admin.ModelAdmin):
    pass


class FoodGroupAdmin(admin.ModelAdmin):
    pass


class FoodProductNutrientInlineAdmin(admin.TabularInline):
    model = FoodProductNutrient


class FoodProductUnitInlinAdmin(admin.TabularInline):
    model = FoodProductUnit


class FoodProductAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'food_source', 'food_group', 'default_unit')
    list_filter = ('food_source', 'food_group')
    search_fields = ('full_name', )
    inlines = (FoodProductUnitInlinAdmin, FoodProductNutrientInlineAdmin)

    def get_nutrients(self, obj):
        nutrients = [str(food_product_nutrient.quantity) + ' ' + str(food_product_nutrient.nutrient) for food_product_nutrient in FoodProductNutrient.objects.filter(product=obj)]

        return '\n'.join(nutrients)

    get_nutrients.short_description = 'Nutrients (per 100)'





admin.site.register(Unit, UnitAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(FoodGroup, FoodGroupAdmin)
admin.site.register(FoodProduct, FoodProductAdmin)

