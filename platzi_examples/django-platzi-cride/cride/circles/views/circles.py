"""Circle views."""
# Recordar que hay un JsonResponse que es de django y es una subclase de HttpResopnse. Ver docs para mas info

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')
    filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all() # Hasta ésta instancia no se hace ninguna query. Sino que se define que de todos los circulos, haga algo...
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )

# Emmedocs
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# # *********************************************************
# # Ejemplo de una instancia anterior al desarrollo final
# # *********************************************************
# @api_view(['GET']) # Este endpoint, sólo puede ser llamado por 'get'
# def list_circles(request):
#     circles = Circle.objects.all() # Aca se traen todos los círculos
#     public = circles.filter(is_public=True) # Aca se emplea un filtro. Hasta éste punto no se obtiene nada, Hasta acá no se hace la query
#     data=[] # Lista que se va llenando con cada query.
#     # Recien cuando se itera, es cuando se ejecuta la query
#     for circle in public:
#         data.append({
#             'name': circle.name,
#             'slug_name': circle.slug_name,
#             'rides_taken': circle.rides_taken,
#             'rides_offered': circle.rides_offered,
#             'members_limit': circle.members_limit,
#         })
#     return Response(data) # Este 'Response' ya parsea automaticamente a json
