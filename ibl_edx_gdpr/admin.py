from django.contrib import admin
from .models import RetirementBackgroundCache

@admin.register(RetirementBackgroundCache)
class TempAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'old_value', 'new_value', 'last_updated')
