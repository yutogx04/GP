from rest_framework import viewsets
from backend.backend.models import candidacy
from .serializers import CandidacySerializer
from .permissions import IsAdminOrReadOnly


class CandidacyViewSet(viewsets.ModelViewSet):
    queryset = candidacy.objects.all()
    serializer_class = CandidacySerializer
    permission_classes = [IsAdminOrReadOnly]
