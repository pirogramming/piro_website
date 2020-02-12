from django.contrib import admin
from .models import Recruitment


@admin.register(Recruitment)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title']
