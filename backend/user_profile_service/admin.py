from django.contrib import admin
from .models import StudentProfile, PieceJustificative, EncadrantProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "numero_etudiant", "niveau_etude", "date_inscription")
    search_fields = ("user__email", "numero_etudiant")

@admin.register(PieceJustificative)
class PieceJustificativeAdmin(admin.ModelAdmin):
    list_display = ("student", "type_piece", "nom_fichier", "date_depot")
    readonly_fields = ("date_depot",)
    search_fields = ("student__user__email", "type_piece", "nom_fichier")

@admin.register(EncadrantProfile)
class EncadrantProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "phone_number")
    search_fields = ("user__email", "department")