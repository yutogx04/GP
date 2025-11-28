from django.urls import path
from .views import (
    OfferListView, OfferDetailView, OfferCreateView, OfferUpdateView, OfferPublishView,
    EstablishmentListCreateView, ServiceHospitalierListCreateView
)

app_name = "internship_offer_service"

urlpatterns = [
    path("offers/", OfferListView.as_view(), name="offer-list"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("offers/create/", OfferCreateView.as_view(), name="offer-create"),
    path("offers/<int:pk>/update/", OfferUpdateView.as_view(), name="offer-update"),
    path("offers/<int:pk>/publish/", OfferPublishView.as_view(), name="offer-publish"),

    path("establishments/", EstablishmentListCreateView.as_view(), name="establishment-list-create"),
    path("services/", ServiceHospitalierListCreateView.as_view(), name="service-list-create"),
]
