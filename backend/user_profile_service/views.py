from rest_framework import viewsets
from backend.backend.models import Doyen
from .serializers import DoyenSerializer
from .permissions import IsAdminOrReadOnly


class DoyenViewSet(viewsets.ModelViewSet):
    queryset = Doyen.objects.all()
    serializer_class = DoyenSerializer
    permission_classes = [IsAdminOrReadOnly]
