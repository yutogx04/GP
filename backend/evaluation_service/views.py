from rest_framework import viewsets
from .models import Evaluation
from .serializers import EvaluationSerializer
from .permissions import IsAdminOrReadOnly


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAdminOrReadOnly]
