from django.contrib import admin
from .models import AssignmentOverride

@admin.register(AssignmentOverride)
class AssignmentOverrideAdmin(admin.ModelAdmin):
    list_display = ("performed_by", "candidacy_id", "created_at")
    list_filter = ("created_at",)
    search_fields = ("performed_by__email", "candidacy_id")