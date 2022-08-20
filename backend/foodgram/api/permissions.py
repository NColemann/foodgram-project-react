from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdminPermission(BasePermission):
    """Доступ к безопасным методам для неавторизованных пользователей
    и полный доступ для авторизованных и админов."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )
