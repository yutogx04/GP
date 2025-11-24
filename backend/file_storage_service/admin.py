from django.contrib import admin
from backend.backend.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'student', 'upload_date')
