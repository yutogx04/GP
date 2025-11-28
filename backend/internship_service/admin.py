from django.contrib import admin
from .models import Stage

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("id", "candidacy", "medecin", "start_date", "end_date", "status")
    list_filter = ("status",)
    search_fields = ("candidacy__id", "medecin__email")