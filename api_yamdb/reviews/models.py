from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER_ROLE = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    )
    bio = models.TextField(
        verbose_name='Biography',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='User Email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='User role',
        max_length=15,
        choices=USER_ROLE,
        default='user',
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование категории"
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True,
        verbose_name="slug категории"
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование жанра"
    )
    slug = models.SlugField(max_length=50, unique=True,
                            blank=True,
                            verbose_name="slug жанра")

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name="Наименование произведения",
        max_length=200
    )
    year = models.IntegerField(
        blank=True,
        default=0,
        db_index=True,
        verbose_name="Год выпуска")
    description = models.CharField(
        blank=True, verbose_name="Описание", max_length=200
    )
    genre = models.ManyToManyField(
        Genres,
        related_name="titles",
        blank=True,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )
    rating = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True, )
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True, )


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, message='Максимальная оценка 10'),
            MinValueValidator(1, message='Минимальная оценка 1')
        ]
    )

    class Meta:
        unique_together = ('author', 'title')
        ordering = ('id',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.text
