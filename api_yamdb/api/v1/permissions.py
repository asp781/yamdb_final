from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Определение прав для роли Администратор."""

    def has_permission(self, request, view):
        """Функция определяет права на уровне запроса и пользователя."""
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_staff
        )


class IsModeratorAdmin(permissions.BasePermission):
    """Определение прав для роли Модератор."""

    def has_permission(self, request, view):
        """Функция определяет права на уровне запроса и пользователя."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Функция определяет права на уровне объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
            or request.user.is_moderator or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Определение прав для анонимного пользователя."""

    def has_permission(self, request, view):
        """Функция определяет права на уровне запроса и пользователя."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        """Функция определяет права на уровне объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_staff
        )
