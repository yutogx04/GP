from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

app_name = 'student_service' 

urlpatterns = [
    path('', include(DefaultRouter().urls)),
]
