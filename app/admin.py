from django.contrib import admin
from .models import AttendanceModels


class AttendanceModelsAdmin(admin.ModelAdmin):
    list_display = ('user', 'days', 'start', 'end')  # Add or remove fields as needed
    list_filter = ('user', 'days')  # Add filters if necessary
    search_fields = ('user__first_name', 'user__last_name', 'days__date')  # Add fields for search

admin.site.register(AttendanceModels, AttendanceModelsAdmin)