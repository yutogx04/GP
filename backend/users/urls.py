from django.urls import path
from .views import (
    StudentProfileView, DocumentUploadView, DocumentDetailView,
    AcademicHistoryView, AcademicHistoryDetailView,
    complete_profile, profile_health,
    HospitalStaffListView, HospitalStaffCreateView, HospitalStaffDetailView,
    SupervisorStudentListView,
    FacultyStudentListView, FacultyStudentCreateView, FacultyStudentDetailView,
    FacultyReportsView,
    ConversationListView, ConversationMessagesView,
    toggle_user_active, reset_user_password
)
from .availability_views import (
    AvailabilityListCreateView, AvailabilityDetailView,
    UnavailableDateListCreateView, UnavailableDateDetailView
)

urlpatterns = [
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
    path('profile/complete/', complete_profile, name='complete-profile'),
    path('profile/health/', profile_health, name='profile-health'),
    path('documents/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('academic-history/', AcademicHistoryView.as_view(), name='academic-history'),
    path('academic-history/<int:pk>/', AcademicHistoryDetailView.as_view(), name='academic-history-detail'),
    
    path('hospital-staff/', HospitalStaffListView.as_view(), name='hospital-staff-list'),
    path('hospital-staff/create/', HospitalStaffCreateView.as_view(), name='hospital-staff-create'),
    path('hospital-staff/<int:pk>/', HospitalStaffDetailView.as_view(), name='hospital-staff-detail'),
    
    path('supervisor/students/', SupervisorStudentListView.as_view(), name='supervisor-students'),
    
    path('faculty/students/', FacultyStudentListView.as_view(), name='faculty-students'),
    path('faculty/students/create/', FacultyStudentCreateView.as_view(), name='faculty-student-create'),
    path('faculty/students/<int:pk>/', FacultyStudentDetailView.as_view(), name='faculty-student-detail'),
    path('faculty/reports/', FacultyReportsView.as_view(), name='faculty-reports'),
    
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
    
    path('<int:pk>/toggle-active/', toggle_user_active, name='toggle-user-active'),
    path('<int:pk>/reset-password/', reset_user_password, name='reset-user-password'),
    
    path('availability/', AvailabilityListCreateView.as_view(), name='availability-list'),
    path('availability/<int:pk>/', AvailabilityDetailView.as_view(), name='availability-detail'),
    path('availability/dates/', UnavailableDateListCreateView.as_view(), name='unavailable-dates-list'),
    path('availability/dates/<int:pk>/', UnavailableDateDetailView.as_view(), name='unavailable-dates-detail'),
]