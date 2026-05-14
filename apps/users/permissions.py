from rest_framework import permissions 


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return True

        return (
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user or
            request.user.is_superuser
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name="Admin").exists()
        )


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name="Customer").exists()
        )


class IsStaffGroup(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name="Staff").exists()
        )
