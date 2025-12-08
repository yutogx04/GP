from django.contrib import admin
from .models import Hospital, HospitalAdmin

@admin.register(Hospital)
class HospitalModelAdmin(admin.ModelAdmin):  # Changed from HospitalAdmin to HospitalModelAdmin
    list_display = ('name', 'hospital_type', 'city', 'state', 'is_active')
    list_filter = ('hospital_type', 'city', 'state', 'is_active')
    search_fields = ('name', 'city', 'state')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HospitalAdmin)
class HospitalAdminModelAdmin(admin.ModelAdmin):  # Changed from HospitalAdminAdmin to HospitalAdminModelAdmin
    list_display = ('user', 'hospital', 'position', 'is_active')
    list_filter = ('is_active', 'hospital')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'hospital__name')