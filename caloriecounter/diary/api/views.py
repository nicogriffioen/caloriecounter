from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from caloriecounter.diary.api.serializers import DiaryEntrySerializer
from caloriecounter.diary.models import DiaryEntry


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
    filterset_fields = ['date']

    def get_queryset(self):
        user = self.request.user
        return DiaryEntry.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)