from django.db.models import Count

from .models import Category


def categories(request):
    """
    Контекстный процессор, который добавляет все категории в контекст шаблона
    """
    return {
        "categories": Category.objects.all(),
    }


def top_categories(request):
    """
    Контекстный процессор, который добавляет топ-5 категорий с наибольшим количеством статей в контекст шаблона
    """
    categories = Category.objects.annotate(articles_count=Count("articles")).order_by(
        "-articles_count"
    )[:7]

    return {
        "top_categories": categories,
    }
