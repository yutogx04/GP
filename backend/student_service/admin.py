from django.contrib import admin
from backend.backend.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prenom', 'email', 'actif_status')
