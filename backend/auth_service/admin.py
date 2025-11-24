from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Ensure we don't try to register User twice (Django's auth app may already
# register it). If it's registered, unregister first.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class DjangoUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
