from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import News, Comment, Profile, Picture


# @admin.register(Metatag)
# class MetatagAdmin(admin.ModelAdmin):
#     list_display = ['descriptor']


class CommentInLine(admin.TabularInline):
    model = Comment


class PictureInLine(admin.StackedInline):
    model = Picture


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'create_at', 'status', 'user']
    list_filter = ['status']
    inlines = [CommentInLine, PictureInLine]

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(status=True)
    activate.short_description = "Активировать"

    def deactivate(self, request, queryset):
        queryset.update(status=False)
    deactivate.short_description = "Дективировать"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'short_description']
    list_filter = ['user']
    actions = ['mark_delete']

    def mark_delete(self, request, queryset):
        queryset.update(text='Удаленно администратором')

    mark_delete.short_description = "пометить на удаление"


@admin.register(Picture)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['news', 'image']


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
