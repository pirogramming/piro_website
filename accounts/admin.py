from django.contrib import admin
from .models import PiroUser


@admin.register(PiroUser)
class PiroUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','username', 'piro_no', 'email', 'phone_no', 'is_active')
    list_display_links = ['name', 'username']