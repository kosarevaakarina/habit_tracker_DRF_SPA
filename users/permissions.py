from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """ Проверка прав пользователя"""
    def has_permission(self, request, view):
        return request.user == view.get_object()
