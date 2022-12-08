from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Categories, Genres, Review, Title, User

from .filters import TitleModelFilter
from .permissions import (
    IsAdmin,
    IsModeratorAdmin,
    IsAdminOrReadOnly
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    ReadOnlyTitleSerializer,
    MeSerializer,
    UserSerializer,
    TokenGeneratorSerialiser,
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    UserCreationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """Вью класс для модели User."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Функция для изменения данных своей учетной записи."""
        if request.method == 'PATCH':
            user = request.user
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    """Функция для отправки кода подтверждения."""
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Токен подтверждения', confirmation_code,
              settings.SERVICE_EMAIL, [user.email]
              )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Функция для получения токена."""
    serializer = TokenGeneratorSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetPostMixins(
    DestroyModelMixin,
    CreateModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet
):
    """Определение методов для обработки модели Category."""

    pass


class CategoryViewSet(DetPostMixins):
    """Вью класс для модели Category."""

    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenryViewSet(DetPostMixins):
    """Вью класс для модели Genre."""

    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вью класс для модели Title."""

    queryset = Title.objects.all().annotate(Avg('reviews__score')).order_by(
        'id'
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleModelFilter

    def get_serializer_class(self):
        """Функция для определения сериализатора."""
        if self.action in ('list', 'retrieve'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вью класс для модели Title."""

    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAdmin,)

    def get_queryset(self):
        """Получаем id title."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Функция сохраняет информацию в БД."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вью класс для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsModeratorAdmin,)

    def get_queryset(self):
        """Получаем id review."""
        review = get_object_or_404(Review, id=self.kwargs.get('reviews_id'),
                                   title_id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Функция сохраняет информацию в БД."""
        review = get_object_or_404(Review, pk=self.kwargs.get('reviews_id'))
        serializer.save(author=self.request.user, review=review)
