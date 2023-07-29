from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Проверка прав автора публикации"""

    def has_object_permission(self, request, view, obj):
        """Автор публикации может редактировать и удалять только свои объекты"""
        if request.user == obj.user:
            return request.method in ['PUT', 'PATCH', 'DELETE']

        return False
