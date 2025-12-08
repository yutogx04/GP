from django.urls import path
from .views import (
    HospitalListView, HospitalDetailView, 
    HospitalAdminListView, HospitalAdminDetailView
)

urlpatterns = [
    path('', HospitalListView.as_view(), name='hospital-list'),
    path('<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('admins/', HospitalAdminListView.as_view(), name='hospital-admin-list'),
    path('admins/<int:pk>/', HospitalAdminDetailView.as_view(), name='hospital-admin-detail'),
]