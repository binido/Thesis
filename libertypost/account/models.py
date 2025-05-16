import os
import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def get_random_avatar():
    """
    Функция для получения случайной аватарки из папки avatars
    """
    avatars_dir = os.path.join("media", "avatars")

    if not os.path.exists(avatars_dir):
        return "avatars/default.png"

    avatars = [
        f
        for f in os.listdir(avatars_dir)
        if os.path.isfile(os.path.join(avatars_dir, f))
    ]

    if not avatars:
        return "avatars/default.png"

    random_avatar = random.choice(avatars)

    return os.path.join("avatars", random_avatar)


class User(AbstractUser):
    """
    Кастомная модель пользователя с добавленным полем аватарки
    """

    image = models.ImageField(
        upload_to="avatars/", default=get_random_avatar, verbose_name="Аватарка"
    )

    REQUIRED_FIELDS = ["email"]

    def get_absolute_url(self):
        return reverse("account:user_profile", kwargs={"user_id": self.pk})

    def __str__(self):
        return self.username
