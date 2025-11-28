from django.contrib import admin
from .models import Candidacy

@admin.register(Candidacy)
class CandidacyAdmin(admin.ModelAdmin):
    list_display = ("student", "offer", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("student__email", "offer__title")
    ordering = ("-applied_at",)