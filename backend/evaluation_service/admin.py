from django.contrib import admin
from .models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "stage", "medecin", "date_evaluation")
    list_filter = ("date_evaluation",)
    search_fields = ("stage__id", "medecin__email")