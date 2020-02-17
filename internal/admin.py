from django.contrib import admin
from .models import Post, Comment, Like, InfoBook, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_display_links = ['title']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post','author']
    list_display_links = ['id']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment']
    list_display_links = ['id']

@admin.register(InfoBook)
class InfoBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'piro_no']
    list_display_links = ['id']

