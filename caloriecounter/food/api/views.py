from rest_framework import viewsets, pagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from caloriecounter.food.api.serializers import FoodProductSerializer, NutrientSerializer, FoodGroupSerializer, \
    UnitSerializer
from caloriecounter.food.models import FoodProduct, Nutrient, Unit, FoodGroup


class LargePagination(pagination.PageNumberPagination):
    page_size = 1000


class FoodGroupViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows FoodGroups to be viewed.
    """
    queryset = FoodGroup.objects.all()
    serializer_class = FoodGroupSerializer
    pagination_class = LargePagination


class FoodProductViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows FoodProducts to be viewed.
    """
    queryset = FoodProduct.objects.prefetch_related('foodproductnutrient_set').prefetch_related('units').all()
    serializer_class = FoodProductSerializer


class NutrientViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows Nutrients to be viewed.
    """
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    pagination_class = LargePagination


class UnitViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows Units to be viewed.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    pagination_class = LargePagination
