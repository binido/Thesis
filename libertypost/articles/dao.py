from django.db.models import Q, Count, Prefetch, F, OuterRef, Subquery
from .models import Article, Category, Comment, User
from django.shortcuts import get_object_or_404
from typing import List, Dict, Any, Optional, Union, Tuple
from django.core.paginator import Paginator
from django.db import transaction


class ArticleDAO:
    """
    Data Access Object для работы с моделью статей и связанными моделями.
    Все методы статические, создавать экземпляр класса не нужно.
    """

    @staticmethod
    def get_articles_with_comment_count(
        page: int = 1, per_page: int = 10, status: str = "published"
    ) -> Dict[str, Any]:
        """
        Получить список статей с подсчетом количества комментариев

        Args:
            page: Номер страницы
            per_page: Количество статей на страницу
            status: Статус статей для фильтрации

        Returns:
            Словарь со статьями, их количеством комментариев и информацией о пагинации
        """
        queryset = (
            Article.objects.select_related("author")
            .filter(status=status)
            .annotate(comment_count=Count("comments"))
        )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def get_article_by_id(
        article_id: int,
        prefetch_comments: bool = False,
        prefetch_categories: bool = False,
    ) -> Article:
        """
        Получить статью по ID с возможностью предварительной загрузки комментариев и категорий

        Args:
            article_id: ID статьи
            prefetch_comments: Загружать ли комментарии вместе со статьей
            prefetch_categories: Загружать ли категории вместе со статьей

        Returns:
            Объект статьи или 404 ошибка, если статья не найдена
        """
        queryset = Article.objects.select_related("author")

        if prefetch_comments:
            queryset = queryset.prefetch_related(
                Prefetch("comments", queryset=Comment.objects.select_related("author"))
            )

        if prefetch_categories:
            queryset = queryset.prefetch_related("categories")

        # Добавляем подсчет комментариев
        queryset = queryset.annotate(comment_count=Count("comments"))

        return get_object_or_404(queryset, id=article_id)

    @staticmethod
    def get_articles_by_author(
        author_id: int, status: Optional[str] = None, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Получить статьи конкретного автора с фильтрацией по статусу и пагинацией

        Args:
            author_id: ID автора
            status: Статус статей для фильтрации (если None - все статьи)
            page: Номер страницы для пагинации
            per_page: Количество статей на страницу

        Returns:
            Словарь с объектами статей и информацией о пагинации
        """
        queryset = Article.objects.select_related("author").filter(author_id=author_id)

        if status:
            queryset = queryset.filter(status=status)

        # Добавляем подсчет комментариев
        queryset = queryset.annotate(comment_count=Count("comments"))

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def get_articles_by_status(
        status: str, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Получить все статьи с определенным статусом

        Args:
            status: Статус статей ("moderated", "published", "rejected")
            page: Номер страницы
            per_page: Количество статей на страницу

        Returns:
            Словарь с объектами статей и информацией о пагинации
        """
        queryset = (
            Article.objects.select_related("author")
            .filter(status=status)
            .annotate(comment_count=Count("comments"))
        )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def get_articles_by_category(
        category_slug: str, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Получить опубликованные статьи по категории

        Args:
            category_slug: Slug категории
            page: Номер страницы
            per_page: Количество статей на страницу

        Returns:
            Словарь с объектами статей, категорией и информацией о пагинации
        """
        category = get_object_or_404(Category, slug=category_slug)
        queryset = (
            Article.objects.select_related("author")
            .filter(categories=category, status="published")
            .annotate(comment_count=Count("comments"))
        )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "category": category,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def search_articles(
        query: str, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Поиск статей по заголовку и содержимому

        Args:
            query: Поисковый запрос
            page: Номер страницы
            per_page: Количество статей на страницу

        Returns:
            Словарь с результатами поиска и информацией о пагинации
        """
        queryset = (
            Article.objects.select_related("author")
            .filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                status="published",
            )
            .annotate(comment_count=Count("comments"))
        )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "query": query,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def get_article_comment_count(article_id: int) -> int:
        """
        Получить количество комментариев для конкретной статьи

        Args:
            article_id: ID статьи

        Returns:
            Количество комментариев
        """
        return Comment.objects.filter(article_id=article_id).count()

    @staticmethod
    def get_articles_with_most_comments(limit: int = 5) -> List[Article]:
        """
        Получить статьи с наибольшим количеством комментариев

        Args:
            limit: Количество статей для получения

        Returns:
            Список статей с полем comment_count
        """
        return (
            Article.objects.filter(status="published")
            .annotate(comment_count=Count("comments"))
            .order_by("-comment_count")[:limit]
        )

    @staticmethod
    def get_articles_without_comments(
        page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Получить опубликованные статьи без комментариев

        Args:
            page: Номер страницы
            per_page: Количество статей на страницу

        Returns:
            Словарь со статьями без комментариев и информацией о пагинации
        """
        queryset = (
            Article.objects.filter(status="published", comments__isnull=True)
            .select_related("author")
            .distinct()
        )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "articles": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_articles": paginator.count,
        }

    @staticmethod
    def get_popular_articles(limit: int = 5) -> List[Article]:
        """
        Получить популярные статьи на основе количества комментариев

        Args:
            limit: Количество статей для получения

        Returns:
            Список популярных статей
        """
        return (
            Article.objects.select_related("author")
            .filter(status="published")
            .annotate(comment_count=Count("comments"))
            .order_by("-comment_count")[:limit]
        )

    @staticmethod
    def create_article(
        author_id: int,
        title: str,
        content: str,
        category_ids: List[int],
        source: str,
        image=None,
        status: str = "moderated",
    ) -> Article:
        """
        Создать новую статью

        Args:
            author_id: ID автора
            title: Заголовок статьи
            content: Содержание статьи
            category_ids: Список ID категорий
            source: URL источника статьи
            image: Изображение для статьи (необязательно)
            status: Статус статьи

        Returns:
            Созданная статья
        """
        with transaction.atomic():
            article = Article.objects.create(
                author_id=author_id,
                title=title,
                content=content,
                source=source,
                image=image,
                status=status,
            )

            if category_ids:
                article.categories.set(category_ids)

            return article

    @staticmethod
    def update_article(
        article_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        category_ids: Optional[List[int]] = None,
        source: Optional[str] = None,
        image=None,
        status: Optional[str] = None,
    ) -> Article:
        """
        Обновить существующую статью

        Args:
            article_id: ID статьи
            title: Новый заголовок (если None, не изменится)
            content: Новое содержание (если None, не изменится)
            category_ids: Новый список ID категорий (если None, не изменится)
            source: Новый URL источника (если None, не изменится)
            image: Новое изображение (если None, не изменится)
            status: Новый статус (если None, не изменится)

        Returns:
            Обновленная статья
        """
        with transaction.atomic():
            article = get_object_or_404(Article, id=article_id)

            if title is not None:
                article.title = title

            if content is not None:
                article.content = content

            if source is not None:
                article.source = source

            if image is not None:
                article.image = image

            if status is not None:
                article.status = status

            if category_ids is not None:
                article.categories.set(category_ids)

            article.save()
            return article

    @staticmethod
    def delete_article(article_id: int) -> bool:
        """
        Удалить статью по ID

        Args:
            article_id: ID статьи

        Returns:
            True если статья успешно удалена
        """
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return True


class CategoryDAO:
    """
    Data Access Object для работы с категориями статей
    """

    @staticmethod
    def get_all_categories() -> List[Category]:
        """
        Получить все категории

        Returns:
            Список всех категорий
        """
        return Category.objects.all()

    @staticmethod
    def get_categories_with_article_count() -> List[Dict[str, Any]]:
        """
        Получить все категории с количеством опубликованных статей

        Returns:
            Список категорий с количеством статей
        """
        return Category.objects.annotate(
            article_count=Count("articles", filter=Q(articles__status="published"))
        ).values("id", "name", "slug", "article_count")

    @staticmethod
    def get_category_by_slug(slug: str) -> Category:
        """
        Получить категорию по slug

        Args:
            slug: Slug категории

        Returns:
            Объект категории или 404 ошибка
        """
        return get_object_or_404(Category, slug=slug)


class CommentDAO:
    """
    Data Access Object для работы с комментариями
    """

    @staticmethod
    def get_comments_for_article(
        article_id: int, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Получить комментарии для статьи с пагинацией

        Args:
            article_id: ID статьи
            page: Номер страницы
            per_page: Количество комментариев на страницу

        Returns:
            Словарь с комментариями и информацией о пагинации
        """
        queryset = Comment.objects.select_related("author").filter(
            article_id=article_id
        )
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)

        return {
            "comments": page_obj.object_list,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "total_comments": paginator.count,
        }

    @staticmethod
    def create_comment(article_id: int, author_id: int, content: str) -> Comment:
        """
        Создать новый комментарий

        Args:
            article_id: ID статьи
            author_id: ID автора
            content: Текст комментария

        Returns:
            Созданный комментарий
        """
        article = get_object_or_404(Article, id=article_id)

        return Comment.objects.create(
            article=article, author_id=author_id, content=content
        )

    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """
        Удалить комментарий по ID

        Args:
            comment_id: ID комментария

        Returns:
            True если комментарий успешно удален
        """
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return True


class UserDAO:
    """
    Data Access Object для работы с пользователями в контексте статей
    """

    @staticmethod
    def get_top_authors(limit: int = 5) -> List[Dict[str, Any]]:
        """
        Получить топ авторов по количеству опубликованных статей

        Args:
            limit: Количество авторов для получения

        Returns:
            Список авторов с информацией о количестве статей
        """
        return (
            User.objects.annotate(
                published_articles=Count(
                    "articles", filter=Q(articles__status="published")
                )
            )
            .filter(published_articles__gt=0)
            .order_by("-published_articles")[:limit]
        )

    @staticmethod
    def get_author_stats(author_id: int) -> Dict[str, int]:
        """
        Получить статистику автора по статьям

        Args:
            author_id: ID автора

        Returns:
            Словарь со статистикой
        """
        author = get_object_or_404(User, id=author_id)

        published_count = Article.objects.filter(
            author=author, status="published"
        ).count()

        moderated_count = Article.objects.filter(
            author=author, status="moderated"
        ).count()

        rejected_count = Article.objects.filter(
            author=author, status="rejected"
        ).count()

        comments_count = Comment.objects.filter(author=author).count()

        return {
            "published_count": published_count,
            "moderated_count": moderated_count,
            "rejected_count": rejected_count,
            "total_articles": published_count + moderated_count + rejected_count,
            "comments_count": comments_count,
        }
