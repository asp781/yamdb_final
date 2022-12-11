from django.contrib import admin

from .models import (Categories, Comment, Genres, GenreTitle, Review, Title,
                     User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role', 'email')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'rating', 'year', 'category')


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'title_id', 'author', 'text', 'pub_date', 'score'
    )
    list_filter = ('author',)
    search_fields = ('author', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'review_id', 'review')
    list_filter = ('author',)
    search_fields = ('author', 'pub_date')


@admin.register(GenreTitle)
class GenreTitle(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'title', 'genre_id', 'genre')
