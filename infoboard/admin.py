from django.contrib import admin

from infoboard.models import Info, Files


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    list_display_links = ['id']
    search_fields = ['title']
    list_filter = ('user__name',)


@admin.register(Files)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'info', 'filename']
    list_display_links = ['id']
    search_fields = ['info__title']
    list_filter = ('filename',)
