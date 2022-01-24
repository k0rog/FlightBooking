from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsAdminOrProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.kwargs['pk'] == request.user.id:
            view.kwargs['self_user'] = True
            return True

        if request.user.groups.filter(name='admin').exists():
            return True

        return False


class IsAdmin(permissions.BasePermission):
    message = _('This action is only for admins')

    def has_permission(self, request, view):
        if request.user.groups.filter(name='admin').exists():
            return True

        return False


class IsOwner(permissions.BasePermission):
    message = _('This action is only for profile owners')

    def has_permission(self, request, view):
        if view.kwargs['pk'] == request.user.id:
            view.kwargs['self_user'] = True
            return True

        return False


class IsPassenger(permissions.BasePermission):
    message = _('This action is only for passengers')

    def has_permission(self, request, view):
        if request.user.groups.filter(name='passenger').exists():
            return True

        return False
