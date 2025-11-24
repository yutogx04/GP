from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer
from .permissions import IsAdminOrReadOnly


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAdminOrReadOnly]
