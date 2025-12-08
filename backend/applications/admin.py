from django.contrib import admin
from .models import Application, ApplicationDocument


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'offer', 'status', 'applied_at', 'score')
    list_filter = ('status', 'applied_at', 'offer__hospital')
    search_fields = ('student__email', 'offer__title')
    readonly_fields = ('applied_at', 'updated_at')
    date_hierarchy = 'applied_at'


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'name', 'uploaded_at')
    search_fields = ('application__student__email', 'name')