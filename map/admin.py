from django.contrib import admin
from .models import Marker


class AdminMarker(admin.ModelAdmin):
    # list_display = ('name', 'description', 'marker_region', 'creator')
    fieldsets = [
        ('Про проблему', {'fields': ['name', 'description', 'marker_region', 'creator']}),
        ('Статус проблеми', {'fields': ['in_process']}),
    ]
    model = Marker


admin.site.register(Marker, AdminMarker)