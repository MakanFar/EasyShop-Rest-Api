from rest_framework import permissions


class IsOwnerOrNoAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'shop'):
            if obj.shop == request.user.employee.shop:
                return True
        return False