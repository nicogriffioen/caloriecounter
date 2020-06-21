from django.contrib import admin

# Register your models here.
from caloriecounter.diary.models import DiaryEntry


class DiaryEntryAdmin(admin.ModelAdmin):
    readonly_fields = ['created_on', 'nutritional_information']
    fields = ['user', 'created_on','unit', 'portion', 'product', 'quantity', 'nutritional_information', 'date', 'time']
    list_display = ['__str__', 'user', 'created_on']
    autocomplete_fields = ['user', 'product', 'unit', 'portion']


admin.site.register(DiaryEntry, DiaryEntryAdmin)

