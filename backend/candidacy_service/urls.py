from django.urls import path
from .views import ApplyToOfferView, MyCandidaciesListView, OfferApplicationsListView

app_name = "candidacy_service"

urlpatterns = [
    path("apply/", ApplyToOfferView.as_view(), name="apply"),
    path("me/", MyCandidaciesListView.as_view(), name="my-candidacies"),
    path("offers/<int:offer_pk>/applications/", OfferApplicationsListView.as_view(), name="offer-applications"),
]
