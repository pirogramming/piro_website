from django.contrib import admin
from photobook.models import Photobook, Images

@admin.register(Photobook)
class PhotobookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    list_display_links = ['id']
    search_fields = ['title']
    list_filter = ('user__name',)

@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photobook']
    list_display_links = ['id']
    search_fields = ['photobook__title']