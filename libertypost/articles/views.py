import markdown
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .dao import ArticleDAO, CategoryDAO, CommentDAO, UserDAO


def articles(request: HttpRequest) -> HttpResponse:
    page = request.GET.get("page", 1)

    try:
        page = int(page)
    except ValueError:
        page = 1

    articles_data = ArticleDAO.get_articles_with_comment_count(page=page)

    for article in articles_data["articles"]:
        if hasattr(article, "content") and article.content:
            article.html_content = markdown.markdown(article.content)
        else:
            article.html_content = None

    data = {
        "articles": articles_data["articles"],
        "page_obj": articles_data["page_obj"],
        "is_paginated": articles_data["is_paginated"],
        "total_articles": articles_data["total_articles"],
    }

    return render(request, "articles/articles.html", data)


def article(request: HttpRequest, article_id: int) -> HttpResponse:
    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get("comment", "").strip()
        if comment_text:
            CommentDAO.create_comment(
                article_id=article_id, author_id=request.user.id, content=comment_text
            )
        return redirect("articles:article", article_id=article_id)

    article = ArticleDAO.get_article_by_id(
        article_id=article_id, prefetch_comments=True, prefetch_categories=True
    )
    author = UserDAO.get_author_stats(author_id=article.author.id)
    comments = CommentDAO.get_comments_for_article(article_id=article.id)

    content = article.content
    content = markdown.markdown(content) if content else None

    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.id == article.author.id

    data = {
        "article": {
            "id": article.id,
            "title": article.title,
            "content": content,
            "author_name": article.author.username,
            "author_id": article.author.id,
            "author_avatar": article.author.image.url if article.author.image else None,
            "categories": [cat.name for cat in article.categories.all()],
            "image": article.image.url if article.image else None,
            "published_ago": article.created_at,
            "comment_count": article.comment_count,
            "source": article.source,
            "total_articles": author["total_articles"],
            "comments": comments["comments"],
            "url": article.get_absolute_url(),
        },
        "page_obj": comments["page_obj"],
        "is_paginated": comments["is_paginated"],
        "total_comments": comments["total_comments"],
        "is_owner": is_owner,
    }
    return render(request, "articles/article.html", context=data)


@login_required
def create_article(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        source = request.POST.get("link", "").strip()
        category_ids = request.POST.getlist("cats")
        image = request.FILES.get("file")

        if all([title, content, source, category_ids]):
            ArticleDAO.create_article(
                author_id=request.user.id,
                title=title,
                content=content,
                source=source,
                category_ids=[int(c) for c in category_ids],
                image=image,
            )
            return redirect("home")

    return render(request, "articles/create_article.html")


@login_required
def update_article(request: HttpRequest, article_id: int) -> HttpResponse:
    article = ArticleDAO.get_article_by_id(article_id, prefetch_categories=True)

    if request.user.id != article.author.id:
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        source = request.POST.get("link", "").strip()
        category_ids = request.POST.getlist("cats")
        image = request.FILES.get("file")

        if all([title, content, source, category_ids]):
            ArticleDAO.update_article(
                article_id=article_id,
                title=title,
                content=content,
                source=source,
                category_ids=[int(c) for c in category_ids],
                image=image if image else None,
                status="moderated",
            )
            return redirect("home")

    categories = CategoryDAO.get_all_categories()

    current_category_ids = [category.id for category in article.categories.all()]

    context = {
        "article": article,
        "categories": categories,
        "current_category_ids": current_category_ids,
    }

    return render(request, "articles/update_article.html", context=context)


@login_required
def delete_article(request: HttpRequest, article_id: int) -> HttpResponse:
    article = ArticleDAO.get_article_by_id(article_id)

    if request.user.id != article.author.id:
        return redirect("home")

    ArticleDAO.delete_article(article_id)
    return redirect("home")


def category(request: HttpRequest, category_slug: str) -> HttpResponse:
    page = request.GET.get("page", 1)

    try:
        page = int(page)
    except ValueError:
        page = 1

    articles_data = ArticleDAO.get_articles_by_category(
        category_slug=category_slug, page=page
    )

    for article in articles_data["articles"]:
        if hasattr(article, "content") and article.content:
            article.html_content = markdown.markdown(article.content)
        else:
            article.html_content = None

    return render(request, "articles/category.html", context=articles_data)


def search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "")
    sort = request.GET.get("sort", "-created_at")
    category_slug = request.GET.get("category")
    page = request.GET.get("page", 1)

    try:
        page = int(page)
    except ValueError:
        page = 1

    articles_data = ArticleDAO.search_articles(
        query=query, page=page, per_page=10, order_by=sort, category_slug=category_slug
    )

    for article in articles_data["articles"]:
        if hasattr(article, "content") and article.content:
            article.html_content = markdown.markdown(article.content)
        else:
            article.html_content = None

    return render(request, "articles/search.html", context=articles_data)


def page_not_found_view(request: HttpRequest, exception) -> HttpResponse:
    return render(request, "articles/404.html", status=404)
