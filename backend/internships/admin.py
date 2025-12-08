from django.contrib import admin
from .models import InternshipOffer, Internship, InternshipJournal


@admin.register(InternshipOffer)
class InternshipOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'hospital', 'department', 'status', 'validation_status', 'start_date', 'available_slots']
    list_filter = ['status', 'validation_status', 'type', 'hospital']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['student', 'offer', 'supervisor', 'status', 'start_date', 'end_date']
    list_filter = ['status']
    search_fields = ['student__user__email', 'offer__title']


@admin.register(InternshipJournal)
class InternshipJournalAdmin(admin.ModelAdmin):
    list_display = ['internship', 'date', 'created_at']
    list_filter = ['date']
