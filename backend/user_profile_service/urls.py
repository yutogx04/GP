from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DoyenViewSet

router = DefaultRouter()
router.register(r'doyens', DoyenViewSet, basename='doyen')

urlpatterns = [
    path('', include(router.urls)),
]
