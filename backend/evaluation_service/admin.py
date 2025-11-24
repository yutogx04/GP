from django.contrib import admin
from backend.backend.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'evalyation', 'evaluation_date', 'doctor')
