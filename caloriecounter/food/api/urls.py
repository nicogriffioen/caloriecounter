from django.urls import include, path
from rest_framework import routers

from caloriecounter.food.api import views

router = routers.DefaultRouter()
router.register(r'food_group', views.FoodGroupViewSet)
router.register(r'food_product', views.FoodProductViewSet)
router.register(r'nutrient', views.NutrientViewSet)
router.register(r'unit', views.UnitViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]