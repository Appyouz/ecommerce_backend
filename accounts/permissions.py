from typing import override
from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    message = "Only sellers can access this resource."

    @override
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seller()
