import enum
from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(enum.Enum):
    admin = 'admin'
    user = 'user'


class MyUser(AbstractUser):
    CHOICES = (
        (Roles.admin.name, 'Администратор'),
        (Roles.user.name, 'Пользователь'),
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Адрес электронной почты')
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        max_length=150,
    )
    role = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=Roles.user.name,
    )
    class Meta:
        ordering = ('-username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='author',)
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='user',)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
