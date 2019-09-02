from django.contrib import admin

# Register your models here.
from caloriecounter.diary.models import DiaryEntry


class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'created_on']
    autocomplete_fields = ['user', 'product', 'unit']




admin.site.register(DiaryEntry, DiaryEntryAdmin)