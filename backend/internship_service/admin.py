from django.contrib import admin
from backend.backend.models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'doctor', 'status', 'start_date', 'end_date')
