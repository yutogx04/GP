from django.contrib import admin
from .models import Establishment, ServiceHospitalier, Offer

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "contact_email", "phone")

@admin.register(ServiceHospitalier)
class ServiceHospitalierAdmin(admin.ModelAdmin):
    list_display = ("name", "establishment", "capacite_accueil")

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "establishment", "service", "status", "date_publication", "number_places")
    list_filter = ("status", "establishment", "service")
    search_fields = ("title", "description")
    actions = ["publish_offers", "close_offers"]