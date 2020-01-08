from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from caloriecounter.voice.api.serializers import VoiceSessionSerializer
from caloriecounter.voice.models import VoiceSession
from caloriecounter.voice.pipeline import process_session


class VoiceSessionViewSet(viewsets.GenericViewSet,
                          RetrieveModelMixin,
                          CreateModelMixin,
                          UpdateModelMixin,):
    """
    API endpoint that allows Sessions to be viewed and created.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VoiceSessionSerializer

    def get_queryset(self):
        user = self.request.user
        return VoiceSession.objects.prefetch_related('items').filter(user=user)

    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)

        process_session(session)

    def perform_update(self, serializer):
        session = serializer.save()

        process_session(session)