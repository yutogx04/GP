from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'specialty', 'capacity', 'is_active')
    list_filter = ('hospital', 'specialty', 'is_active')
    search_fields = ('name', 'hospital__name', 'specialty')