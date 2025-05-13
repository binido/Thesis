from django.contrib import admin
from .models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author_name",
        "status",
        "created_at",
        "display_categories",
    )
    list_filter = ("status", "categories")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_editable = ("status",)
    filter_horizontal = ("categories",)

    def author_name(self, obj):
        return obj.author.username

    author_name.short_description = "Автор"

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    display_categories.short_description = "Категории"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)
    list_editable = ("slug",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "author", "created_at")
    list_filter = ("article", "author")
    search_fields = ("content",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    def article_title(self, obj):
        return obj.article.title

    article_title.short_description = "Статья"

    def author_name(self, obj):
        return obj.author.username

    author_name.short_description = "Автор"
