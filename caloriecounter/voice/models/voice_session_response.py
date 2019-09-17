import random

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _


class VoiceSessionResponse(models.Model):
    class Meta:
        verbose_name = _('voice session response')

    code = CharField(verbose_name=_('code'), max_length=255, editable=False, unique=True)

    responses = ArrayField(models.TextField(blank=True))

    RESPONSE_OK = 'ok'
    RESPONSE_YES = 'yes'
    RESPONSE_NO = 'no'


responses = [
    (VoiceSessionResponse.RESPONSE_OK, ['OK!', 'Got it!']),
    (VoiceSessionResponse.RESPONSE_YES, ['Yes', 'Yep!']),
    (VoiceSessionResponse.RESPONSE_NO, ['No.', 'Nope!']),
]

def get_response_from_code(code):
    response = VoiceSessionResponse.objects.get(code=code)

    return random.choice(response.responses)

