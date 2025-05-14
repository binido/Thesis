from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


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
            return redirect("home")  # Замените на свой URL
        else:
            # Если форма невалидна, покажем ошибки в шаблоне
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
            username = form.cleaned_data.get(
                "username"
            )  # Может быть email или username
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {user.username}")
                return redirect("home")  # Замените на свой URL
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
    return redirect("login")  # Переадресация на страницу входа


def profile(request):
    pass


def user_profile(request, user_id):
    pass
