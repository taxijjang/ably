from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    작성자만 읽기 및 수정이 가능
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user
