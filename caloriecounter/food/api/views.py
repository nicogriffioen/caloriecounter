from django.contrib.postgres.search import TrigramDistance
from django.db.models import Q, F
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, pagination
from rest_framework.filters import SearchFilter, BaseFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.settings import api_settings

from caloriecounter.food.api.serializers import FoodProductSerializer, NutrientSerializer, FoodGroupSerializer, \
    UnitSerializer, FoodProductCommonNameSerializer
from caloriecounter.food.models import FoodProduct, Nutrient, Unit, FoodGroup, FoodProductCommonName


class TrigramSearchFilterBackend(BaseFilterBackend):
    search_param = api_settings.SEARCH_PARAM

    search_title = _('Search')
    search_description = _('A search term.')

    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """

        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset

        queryset = queryset.annotate(common_name_distance = TrigramDistance('common_names__text', ' '.join(self.get_search_terms(request))))
        queryset = queryset.annotate(common_name=F('common_names'))
        queryset = queryset.annotate(distance=TrigramDistance('full_name', ' '.join(self.get_search_terms(request))))
        queryset = queryset.filter(Q(distance__lte=0.7) | Q(common_name_distance__lte=0.7))
        queryset = queryset.order_by('common_name_distance', 'distance')

        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return coreapi.Field(
            name=self.search_param,
            required=False,
            location='query',
            schema=coreschema.String(
                title=force_str(self.search_title),
                description=force_str(self.search_description)
            )
        )

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.search_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.search_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]


class LargePagination(pagination.PageNumberPagination):
    page_size = 1000


class FoodGroupViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows FoodGroups to be viewed.
    """
    # schema = AutoSchema()
    queryset = FoodGroup.objects.all()
    serializer_class = FoodGroupSerializer
    pagination_class = LargePagination


class FoodProductViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows FoodProducts to be viewed.
    """
    # schema = AutoSchema()
    queryset = FoodProduct.objects\
        .prefetch_related('nutrients')\
        .prefetch_related('units')\
        .prefetch_related('common_names')

    filter_backends = [TrigramSearchFilterBackend]

    serializer_class = FoodProductSerializer


class NutrientViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows Nutrients to be viewed.
    """
    # schema = AutoSchema()
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    pagination_class = LargePagination


class UnitViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    API endpoint that allows Units to be viewed.
    """
    # schema = AutoSchema()
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    pagination_class = LargePagination
