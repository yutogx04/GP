from django.urls import path
from .views import CreateEvaluationView, EvaluationDetailView, EvaluationPdfView

app_name = "evaluation_service"

urlpatterns = [
    path("create/", CreateEvaluationView.as_view(), name="create-evaluation"),
    path("<int:pk>/", EvaluationDetailView.as_view(), name="evaluation-detail"),
    path("<int:pk>/pdf/", EvaluationPdfView.as_view(), name="evaluation-pdf"),
]
