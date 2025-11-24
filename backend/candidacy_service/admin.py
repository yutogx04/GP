from django.contrib import admin
from .models import candidacy


@admin.register(candidacy)
class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'status', 'date_of_application')
