from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from caloriecounter.voice.models.voice_session import VOICE_CHAT_ITEM_TYPES, VoiceSession


class VoiceSessionItem(models.Model):
    class Meta:
        verbose_name = _('voice session item')
        ordering = ['created_on']

    session = models.ForeignKey(verbose_name=('voice session'),
                                to=VoiceSession,
                                related_name='items',
                                on_delete=models.CASCADE,
                                null=False, blank=False)

    created_on = models.DateTimeField(verbose_name=_('created on'), auto_now_add=True)

    user_created = models.BooleanField(verbose_name=_('chat item was created by user'), default=True)
    type = models.CharField(verbose_name=_('type of chat item'),
                            max_length=255,
                            choices=VOICE_CHAT_ITEM_TYPES,
                            null=False, blank=False)

    text = models.TextField(verbose_name=_('text of the chat item'), null=True, blank=True)

    data = JSONField(_('additional data'), null=True, blank=True)