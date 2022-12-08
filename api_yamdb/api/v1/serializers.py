from rest_framework import serializers
from reviews.models import Categories, Comment, Genres, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User аутенцифицированного пользователя."""

    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserCreationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    def validate_email(self, value):
        """Валидатор для email."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Данный email существует.')
        return email

    def validate_username(self, username):
        """Валидатор для username."""
        username = username.lower()
        if username == 'me':
            raise serializers.ValidationError('Данный username запрещен.')
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username существует.'
            )
        return username

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenGeneratorSerialiser(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genres.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Title
        fields = "__all__"


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title только для чтения."""

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Rewiew."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        """Валидация на дублирование отзыва."""
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
