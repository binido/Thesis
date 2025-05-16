from articles.dao import ArticleDAO, UserDAO
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import User


def register_view(request):
    """
    Представление для регистрации новых пользователей
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("home")
        else:
            return render(request, "account/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "account/register.html", {"form": form})


def login_view(request):
    """
    Представление для входа пользователей
    """
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {user.username}")
                return redirect("home")
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = CustomAuthenticationForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    """
    Представление для выхода пользователей
    """
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect("home")


@login_required
def profile(request, status="published"):
    """
    Представление для отображения профиля текущего пользователя.
    Пользователь может просматривать свои статьи с разными статусами.

    Args:
        status: Статус статей для отображения ('published', 'moderated', 'rejected')
    """
    user = request.user
    page = request.GET.get("page", 1)

    result = ArticleDAO.get_articles_by_author(
        author_id=user.id,
        status=status,
        page=int(page),
        per_page=10,
        order_by="-created_at",
    )

    user_stats = UserDAO.get_author_stats(user.id)

    context = {
        "user_profile": user,
        "articles": result["articles"],
        "page_obj": result["page_obj"],
        "is_paginated": result["is_paginated"],
        "total_articles": result["total_articles"],
        "user_stats": user_stats,
        "current_status": status,
        "is_own_profile": True,
    }

    return render(request, "account/profile.html", context)


def user_profile(request, user_id):
    """
    Представление для просмотра профиля другого пользователя.
    Доступны только опубликованные статьи.

    Args:
        user_id: ID пользователя, профиль которого нужно показать
    """
    user = get_object_or_404(User, id=user_id)
    page = request.GET.get("page", 1)

    result = ArticleDAO.get_articles_by_author(
        author_id=user.id,
        status="published",
        page=int(page),
        per_page=10,
        order_by="-created_at",
    )

    user_stats = {
        "published_count": result["total_articles"],
        "moderated_count": 0,
        "rejected_count": 0,
    }

    is_own_profile = request.user.is_authenticated and request.user.id == user.id

    if is_own_profile:
        return redirect("account:profile")

    context = {
        "user_profile": user,
        "articles": result["articles"],
        "page_obj": result["page_obj"],
        "is_paginated": result["is_paginated"],
        "total_articles": result["total_articles"],
        "user_stats": user_stats,
        "current_status": "published",
        "is_own_profile": is_own_profile,
    }

    return render(request, "account/profile.html", context)
