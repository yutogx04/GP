from django.contrib import admin
from backend.models import Establishment, Hospital_service, Doctor


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'email')


@admin.register(Hospital_service)
class HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'establishment', 'capacity')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prenom', 'specialty', 'email', 'is_service_head')
