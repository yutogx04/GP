from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import InternshipAnnouncementViewSet

router = DefaultRouter()
router.register(r'announcements', InternshipAnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
