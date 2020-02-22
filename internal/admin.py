from django.contrib import admin
from .models import Post, Comment, Like, InfoBook, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post','author']
    list_display_links = ['id']
    search_fields = ['post__title']
    list_filter = ('author',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment']
    list_display_links = ['id']
    list_filter = ('user__name',)

@admin.register(InfoBook)
class InfoBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'piro_no']
    list_display_links = ['id']
    search_fields = ['user__name']
    list_filter = ('piro_no',)

