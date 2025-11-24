from django.contrib import admin
from backend.backend.models import Doyen


@admin.register(Doyen)
class DoyenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prenom')
