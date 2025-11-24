from django.contrib import admin
from backend.backend.models import candidacy


@admin.register(candidacy)
class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'status', 'date_of_application')
