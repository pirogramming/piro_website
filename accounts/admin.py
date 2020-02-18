from django.contrib import admin
from .models import PiroUser, Bookmark


def make_active(self, request, queryset):
    queryset.update(is_active=True)
    make_active.short_description = "일괄 활성화"


def make_unactive(self, request, queryset):
    queryset.update(is_active=False)
    make_active.short_description = "일괄 비활성화"


@admin.register(PiroUser)
class PiroUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'piro_no', 'email', 'phone_no', 'is_active')
    list_display_links = ['name', 'username']

    list_filter = ('piro_no', 'is_active')
    search_fields = ['name']
    list_editable = ['is_active']
    actions = [make_active, make_unactive]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'pirouser', 'bookmark_title', 'bookmark_type')
    list_filter = ('pirouser__name',)


admin.site.site_header = "피로그래밍 운영진 전용 포털"
admin.site.site_title = "피로그래밍- 운영진 전용"
admin.site.index_title = "피로그래밍 운영진님 환영합니다."
