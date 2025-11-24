from rest_framework import viewsets
from backend.models import Candidacy
from .serializers import CandidacySerializer
from .permissions import IsAdminOrReadOnly


class CandidacyViewSet(viewsets.ModelViewSet):
    queryset = Candidacy.objects.all()
    serializer_class = CandidacySerializer
    permission_classes = [IsAdminOrReadOnly]
