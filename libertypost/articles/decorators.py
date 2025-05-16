from functools import wraps
from typing import Callable

from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse


def admin_required(view_func: Callable) -> Callable:
    """
    Декоратор, который проверяет, является ли пользователь администратором.
    Если нет, то перенаправляет на страницу входа или показывает сообщение об ошибке.
    """

    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse("articles:articles"))

    return _wrapped_view
