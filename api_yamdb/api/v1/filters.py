import django_filters

from reviews.models import Title


class TitleModelFilter(django_filters.FilterSet):
    """Вью класс для фильтрации Title."""

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    genre = django_filters.CharFilter(field_name="genre__slug")
    category = django_filters.CharFilter(field_name="category__slug")

    class Meta:
        fields = ('name', 'year', 'genre', 'category')
        model = Title
