from django.contrib import admin
from .models import Doyen


@admin.register(Doyen)
class DoyenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prenom')
