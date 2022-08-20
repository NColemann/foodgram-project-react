from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_user


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user],
        verbose_name='Логин',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta(AbstractUser.Meta):
        ordering = ('username',)


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_follows',
                fields=['user', 'author'],
            ),
        ]
