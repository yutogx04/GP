from django.urls import path
from .views import EstablishmentListCreateView, EstablishmentDetailView, ServiceListCreateView, ServiceDetailView

app_name = "establishment_service"

urlpatterns = [
    path("", EstablishmentListCreateView.as_view(), name="establishment-list-create"),
    path("<int:pk>/", EstablishmentDetailView.as_view(), name="establishment-detail"),
    path("services/", ServiceListCreateView.as_view(), name="service-list-create"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
]
