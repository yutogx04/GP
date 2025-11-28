from django.contrib import admin
from .models import Establishment, ServiceHospitalier

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "contact_email")
    filter_horizontal = ("admins",)

@admin.register(ServiceHospitalier)
class ServiceHospitalierAdmin(admin.ModelAdmin):
    list_display = ("name", "establishment", "capacite_accueil")
    list_filter = ("establishment",)