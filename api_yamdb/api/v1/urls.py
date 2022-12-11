from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenryViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                    send_confirmation_code)

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenryViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', send_confirmation_code, name='register'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(auth_patterns)),
]
