from rest_framework import viewsets
from backend.models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrReadOnly


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]
