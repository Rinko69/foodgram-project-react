from django.contrib.auth.models import AbstractUser
from django.db import models


ADMIN = 'admin'
GUEST = 'guest'
USER = 'user'

CHOICES = [
    (ADMIN, 'Administrator'),
    (GUEST, 'Guest'),
    (USER, 'User'),
]


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты')
    role = models.CharField(
        max_length=16,
        choices=CHOICES,
        default=GUEST,
        verbose_name='Тип пользователя')

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_guest(self):
        return self.role == 'guest'

    @property
    def is_user(self):
        return self.role == 'user'


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',)
    user = models.ForeignKey(
        User,
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
