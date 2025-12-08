from django.urls import path
from .views import (
    ApplicationListView, ApplicationDetailView, 
    ApplicationCreateView, ApplicationUpdateView,
    withdraw_application, calculate_assignment_scores,
    bulk_update_status, assignment_board_data, accept_application
)
from .optimization_views import (
    optimization_summary, hospital_performance,
    applications_trend, specialty_demand, full_optimization_report
)

urlpatterns = [
    path('', ApplicationListView.as_view(), name='application-list'),
    path('create/', ApplicationCreateView.as_view(), name='application-create'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('<int:pk>/update/', ApplicationUpdateView.as_view(), name='application-update'),
    path('<int:pk>/accept/', accept_application, name='application-accept'),
    path('<int:pk>/withdraw/', withdraw_application, name='withdraw-application'),
    path('calculate-scores/', calculate_assignment_scores, name='calculate-scores'),
    path('board/', assignment_board_data, name='assignment-board'),
    path('bulk-update/', bulk_update_status, name='bulk-update-status'),
    path('reports/summary/', optimization_summary, name='reports-summary'),
    path('reports/hospitals/', hospital_performance, name='reports-hospitals'),
    path('reports/trend/', applications_trend, name='reports-trend'),
    path('reports/specialty/', specialty_demand, name='reports-specialty'),
    path('reports/full/', full_optimization_report, name='reports-full'),
]