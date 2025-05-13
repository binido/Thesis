from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.timesince import timesince
from .dao import ArticleDAO, CommentDAO, UserDAO
from .models import Comment


def articles(request: HttpRequest) -> HttpResponse:
    articles = ArticleDAO.get_articles_with_comment_count()

    data = {
        "articles": articles["articles"],
    }
    return render(request, "articles/articles.html", data)


def article(request: HttpRequest, article_id: int) -> HttpResponse:
    article = ArticleDAO.get_article_by_id(
        article_id=article_id, prefetch_comments=True, prefetch_categories=True
    )
    author = UserDAO.get_author_stats(
                author_id=article.author.id
            )
    comments = CommentDAO.get_comments_for_article(article_id=article.id)

    data = {
        "article": {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author_name": article.author.username,
            "author_avatar": article.author.image.url if article.author.image else None,
            "categories": [cat.name for cat in article.categories.all()],
            "image": article.image.url if article.image else None,
            "published_ago": timesince(article.created_at) + " назад",
            "comment_count": article.comment_count,
            "source": article.source,
            "total_articles": author["total_articles"],
            "comments": comments["comments"],
        }
    }
    return render(request, "articles/article.html", context=data)


def create_article(request: HttpRequest) -> HttpResponse:
    data = {"form": {}}
    return render(request, "articles/create_article.html", context=data)


def update_article(request: HttpRequest, article_id: int) -> HttpResponse:
    data = {"form": {}, "article": {"id": article_id}}
    return render(request, "articles/update_article.html", context=data)


def delete_article(request: HttpRequest, article_id: int) -> HttpResponse:
    data = {"article": {"id": article_id}}
    return render(request, "articles/delete_article.html", context=data)


def category(request: HttpRequest, category_slug: str) -> HttpResponse:
    data = {"category": {"slug": category_slug}, "articles": []}
    return render(request, "articles/category.html", context=data)


def search(request: HttpRequest) -> HttpResponse:
    data = {"query": request.GET.get("q", ""), "articles": []}
    return render(request, "articles/search.html", context=data)
