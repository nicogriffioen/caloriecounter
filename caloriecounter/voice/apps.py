from django.apps import AppConfig
from django.db import ProgrammingError


class VoiceConfig(AppConfig):
    name = 'caloriecounter.voice'

    def ready(self):
        # Spacy configuration
        import spacy

        # load any spaCy models that are installed
        # This takes some time to load so doing it here should improve performance
        SUPPORTED_LANGUAGES = ['en']
        LANGUAGE_MODELS = {}

        for language in SUPPORTED_LANGUAGES:
            try:
                #LANGUAGE_MODELS[language] = spacy.load(language)
                pass
            except OSError:
                print('Warning: model {} not found. Run python3 -m spacy download {} and try again.'.format(language,
                                                                                                            language))

        #LANGUAGE_MODELS['en'] = spacy.load('en_core_web_sm')

        # this is used to display the language name
        LANGUAGE_MAPPING = {
            'en': 'English',
        }

        from caloriecounter.voice.models import VoiceSessionResponse
        from .models.voice_session_response import responses
        for response in responses:
            try:
                VoiceSessionResponse.objects.get(code=response[0])
            except VoiceSessionResponse.DoesNotExist as e:
                VoiceSessionResponse.objects.create(code=response[0], responses=response[1])
            except ProgrammingError:
                pass
