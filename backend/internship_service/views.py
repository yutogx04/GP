from rest_framework import viewsets
from .models import Internship
from .serializers import InternshipSerializer
from .permissions import IsAdminOrReadOnly


class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAdminOrReadOnly]
