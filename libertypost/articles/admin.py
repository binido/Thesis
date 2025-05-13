from django.contrib import admin

from .models import Article, Category, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "categories")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_editable = ("status",)
    raw_id_fields = ("author",)
    filter_horizontal = ("categories",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)
    list_editable = ("slug",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "author", "created_at")
    list_filter = ("article", "author")
    search_fields = ("content",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    raw_id_fields = ("article", "author")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
