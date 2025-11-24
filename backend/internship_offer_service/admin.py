from django.contrib import admin
from .models import Internship_announcement


@admin.register(Internship_announcement)
class InternshipAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'publication_date')
