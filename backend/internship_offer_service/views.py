from rest_framework import viewsets
from .models import Internship_announcement
from .serializers import InternshipAnnouncementSerializer
from .permissions import IsAdminOrReadOnly


class InternshipAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Internship_announcement.objects.all()
    serializer_class = InternshipAnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
