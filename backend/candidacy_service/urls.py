from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CandidacyViewSet

router = DefaultRouter()
router.register(r'candidacies', CandidacyViewSet, basename='candidacy')

urlpatterns = [
    path('', include(router.urls)),
]
