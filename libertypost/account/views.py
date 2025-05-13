from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm


def register_view(request):
    """
    Представление для регистрации пользователя
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # При сохранении пользователя аватарка будет выбрана случайно
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")  # Замените на нужный вам URL
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})
