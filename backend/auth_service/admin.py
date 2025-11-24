from django.contrib import admin
from django.contrib.auth.models import User


@admin.register(User)
class DjangoUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
