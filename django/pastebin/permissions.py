from django.http import HttpRequest
from django.views import View

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: View, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
