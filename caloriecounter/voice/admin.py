from django.contrib import admin

from caloriecounter.voice.models import *


class VoiceSessionItemAdmin(admin.TabularInline):
    model = VoiceSessionItem


class VoiceSessionAdmin(admin.ModelAdmin):
    search_fields = ['user__user_name']

    inlines = [VoiceSessionItemAdmin,]


class VoiceSessionResponseAdmin(admin.ModelAdmin):
    pass


admin.site.register(VoiceSession, VoiceSessionAdmin)
admin.site.register(VoiceSessionResponse, VoiceSessionResponseAdmin)

