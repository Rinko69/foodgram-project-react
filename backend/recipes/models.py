from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


H = 'hour'
MIN = 'minutes'

TIME_CHOICES = [
    (H, 'Hour'),
    (MIN, 'Minutes'),
]


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=256,)
    color = ColorField(format="hexa")
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',)
    name = models.CharField(
        max_length=200,
        verbose_name='Название',)
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        through='IngredientRecipe',
        related_name='recipes',)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,)
    text = models.TextField(
        verbose_name='Рецепт',)
    cooking_time = models.IntegerField(
        choices=TIME_CHOICES,
        default=MIN,
        verbose_name='Время приготовления',)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_recipe')
        ]

    def __str__(self):
        return self.text


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredientrecipe',
        on_delete=models.CASCADE,
        verbose_name='Ингридиент')
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredientrecipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Количество',)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'

    def __str__(self):
        return (
            f'{self.ingredient.name} :: {self.ingredient.measurement_unit}'
            f' - {self.amount}'
        )


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user} :: {self.recipe}'


class Favorite(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(FavoriteShoppingCart):

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'shopping_list'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
