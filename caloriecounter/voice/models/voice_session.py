from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid as uuid


class VoiceSession(models.Model):
    class Meta:
        verbose_name = _('voice session')
        ordering = ['uuid']

    uuid = models.UUIDField(verbose_name=_('unique identifier'), primary_key=True, default=uuid.uuid4)
    created_on = models.DateTimeField(verbose_name=_('created on'), auto_now_add=True)

    user = models.ForeignKey(verbose_name=_('user'), to= settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=False)
    user_date = models.DateField(verbose_name=_("user date"), blank=False, null=False)
    user_time = models.TimeField(verbose_name=_("user time"), blank=False, null=False)


VOICE_CHAT_ITEM_TYPES  = [
        ('user_input', _('User input')),
        ('feedback', _('Voice assistant feedback')),
        ('clarification_question', _('Voice assistant clarification question')),
        ('objects_created', _('Object created')),
    ]