# файл: accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Аутентификация по email или имени пользователя
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Проверяем, что пользователь существует по email ИЛИ по username
            user = UserModel.objects.get(Q(email=username) | Q(username=username))
        except UserModel.DoesNotExist:
            return None
        else:
            # Проверяем пароль
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
