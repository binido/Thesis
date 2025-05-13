from django.contrib import admin
from django.utils.html import format_html

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "avatar_preview", "is_staff", "is_active")
    readonly_fields = ("avatar_preview",)

    def avatar_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url
            )
        return "Нет изображения"

    avatar_preview.short_description = "Аватарка"


# Регистрируем модель с кастомным админом
admin.site.register(User, UserAdmin)
