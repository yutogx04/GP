from django.urls import path
from . import views

urlpatterns = [
    path('', views.InternshipOfferListView.as_view(), name='offer-list'),
    path('all/', views.AllOffersListView.as_view(), name='all-offers'),
    path('<int:pk>/', views.InternshipOfferDetailView.as_view(), name='offer-detail'),
    path('create/', views.InternshipOfferCreateView.as_view(), name='offer-create'),
    path('<int:pk>/update/', views.InternshipOfferUpdateView.as_view(), name='offer-update'),
    path('<int:pk>/delete/', views.InternshipOfferDeleteView.as_view(), name='offer-delete'),
    path('<int:pk>/validate/', views.validate_offer, name='offer-validate'),
    path('supervisor/', views.SupervisorInternshipsView.as_view(), name='supervisor-internships'),
    path('hospital/', views.HospitalOffersView.as_view(), name='hospital-offers'),
    path('my-internships/', views.StudentInternshipView.as_view(), name='student-internships'),
    path('schedule/', views.ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedule/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
    path('schedule/export/', views.export_calendar_ical, name='schedule-export'),
    path('import/', views.import_offers, name='offer-import'),
    path('export/', views.export_offers, name='offer-export'),
    path('import/template/', views.import_template, name='import-template'),
    path('placement/<int:pk>/status/', views.update_internship_status, name='update-internship-status'),
    path('placement/<int:internship_id>/journal/', views.JournalListCreateView.as_view(), name='journal-list'),
    path('placement/<int:internship_id>/journal/<int:pk>/', views.JournalDetailView.as_view(), name='journal-detail'),
]
