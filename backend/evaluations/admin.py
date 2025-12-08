from django.contrib import admin
from .models import Evaluation, AutoEvaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('internship', 'supervisor', 'final_grade', 'is_submitted', 'is_validated')
    list_filter = ('is_submitted', 'is_validated', 'evaluation_date')
    search_fields = ('internship__student__user__email', 'supervisor__email')

@admin.register(AutoEvaluation)
class AutoEvaluationAdmin(admin.ModelAdmin):
    list_display = ('internship', 'is_submitted', 'submission_date')
    list_filter = ('is_submitted', 'submission_date')
    search_fields = ('internship__student__user__email',)