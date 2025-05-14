from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User as CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей
    """

    email = forms.EmailField(required=True)
    username = forms.CharField(label="Никнейм")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Пароль еще раз", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        """
        Проверка уникальности email
        """
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма для входа пользователей
    """

    username = forms.CharField(label="Email или Никнейм")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
