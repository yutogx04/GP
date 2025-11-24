from django.contrib import admin
from backend.models import Candidacy

@admin.register(Candidacy)
class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'status', 'date_of_application')
