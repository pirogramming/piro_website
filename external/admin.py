from django.contrib import admin
from .models import Recruitment, Portfolio


@admin.register(Recruitment)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['id']
    search_fields = ['title']

@admin.register(Portfolio)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'pironumber']
    list_display_links = ['id']
    search_fields = ['title']
    list_filter = ('pironumber',)