from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from .utils import process_cover_image

User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles", verbose_name="Автор"
    )
    categories = models.ManyToManyField(
        "Category", related_name="articles", verbose_name="Категории"
    )
    content = models.TextField(verbose_name="Статья")
    status = models.CharField(
        max_length=10,
        choices=[
            ("moderated", "В модерации"),
            ("published", "Опубликовано"),
            ("rejected", "Отклонено"),
            ("archived", "Архивированно"),
        ],
        default="moderated",
        verbose_name="Статус",
    )
    source = models.URLField(
        max_length=200, verbose_name="Источник", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="articles/images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    rejection_reason = models.TextField(
        verbose_name="Причина отклонения", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ["-created_at"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:article", args=[self.id])

    def save(self, *args, **kwargs):
        if self.image:
            try:
                old_instance = Article.objects.get(pk=self.pk) if self.pk else None

                if not old_instance or old_instance.image != self.image:
                    self.image = process_cover_image(self.image)
            except Article.DoesNotExist:
                self.image = process_cover_image(self.image)

        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL-адрес")

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("articles:category", args=[self.slug])


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Статья",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"
