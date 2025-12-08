from django.urls import path
from . import views
from .signature_views import add_signature, get_signatures, delete_signature

urlpatterns = [
    path('', views.EvaluationListView.as_view(), name='evaluation-list'),
    path('student/', views.StudentEvaluationsView.as_view(), name='student-evaluations'),
    path('supervisor/', views.SupervisorEvaluationsView.as_view(), name='supervisor-evaluations'),
    path('<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation-detail'),
    path('create/', views.EvaluationCreateView.as_view(), name='evaluation-create'),
    path('<int:pk>/validate/', views.validate_evaluation, name='evaluation-validate'),
    path('<int:pk>/pdf/', views.download_evaluation_pdf, name='evaluation-pdf'),
    path('<int:evaluation_id>/signatures/', get_signatures, name='evaluation-signatures'),
    path('<int:evaluation_id>/signatures/add/', add_signature, name='add-signature'),
    path('<int:evaluation_id>/signatures/<str:signer_type>/', delete_signature, name='delete-signature'),
]
