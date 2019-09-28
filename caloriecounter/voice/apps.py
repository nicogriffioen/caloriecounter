from django.apps import AppConfig
from django.db import ProgrammingError


class VoiceConfig(AppConfig):
    name = 'caloriecounter.voice'

    def ready(self):
        from caloriecounter.voice.models import VoiceSessionResponse
        from .models.voice_session_response import responses
        for response in responses:
            try:
                VoiceSessionResponse.objects.get(code=response[0])
            except VoiceSessionResponse.DoesNotExist as e:
                VoiceSessionResponse.objects.create(code=response[0], responses=response[1])
            except ProgrammingError:
                pass
