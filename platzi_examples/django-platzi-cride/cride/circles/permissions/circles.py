"""Circles permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow access only to circle admins."""

# se sobreescribe el metodo "has_object_permission" que recibe "(self, request, view, obj)" el objeto es el que trae el view set.
# Hay mas info en la docu: https://www.django-rest-framework.org/api-guide/viewsets/#introspecting-viewset-actions
# tambien se pueden establecer permisos de acuerdo a los "actions" tambien
    def has_object_permission(self, request, view, obj):
        """Verify user have a membership in the obj."""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
