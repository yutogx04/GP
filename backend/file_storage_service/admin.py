from django.contrib import admin
from .models import StoredFile

@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ("id", "uploader", "file", "size", "created_at")
    list_filter = ("created_at", "uploader")
    search_fields = ("uploader__username", "file")