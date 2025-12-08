from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, MarkAllReadView
from .admin_views import (
    EmailTemplateListCreateView, EmailTemplateDetailView,
    CommunicationLogListView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', MarkAllReadView.as_view(), name='notification-mark-all-read'),
    
    path('templates/', EmailTemplateListCreateView.as_view(), name='email-template-list'),
    path('templates/<int:pk>/', EmailTemplateDetailView.as_view(), name='email-template-detail'),
    
    path('logs/', CommunicationLogListView.as_view(), name='communication-log-list'),
]
