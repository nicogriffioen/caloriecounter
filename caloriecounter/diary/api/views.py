from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas.openapi import AutoSchema

from caloriecounter.diary.api.serializers import DiaryEntrySerializer
from caloriecounter.diary.models import DiaryEntry

from django_filters.rest_framework import DjangoFilterBackend


class DiaryEntryViewSet(viewsets.GenericViewSet,
                        ListModelMixin,
                        RetrieveModelMixin,
                        CreateModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin):
    """
    API endpoint that allows DiaryEntries to be viewed, and created.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DiaryEntrySerializer
    filterset_fields = ('date',)

    # schema = AutoSchema()

    def get_queryset(self):
        try:
            user = self.request.user
        except AttributeError as e:
            return DiaryEntry.objects.none()

        return DiaryEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)