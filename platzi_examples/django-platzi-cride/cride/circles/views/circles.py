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

# La explicacion de View sets esta en la view set de "user"
# Aca "CircleViewSet" recibe todos los mixins.
# Para los DELETE por convencion no se devuelve contenido sino que se responde un status 204 de "no content"

# En este ejemplo tambien se limita el "update" solo a los admins y se quita la posibilidad de borrrar circlos. En un primer desarrollo
# el estaba "class CircleViewSet(ModelViewSet)", pero si vamos al fuente, "ModelViewSet" hereda de todos los mixins y de generic view set.
# Ej: class ModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
# Entonces para limitar los mixins que se va a hacer, al "CircleViewSet", en lugar de pasarle el "ModelViewSet" con todos los mixins que
# hereda, simplemente se le pasa los mixins que se va a usar, excepto el de "DestroyModelMixin" para impedir que borren los circulos.

class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, 
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer # indica que serializer va a recibir
    # La ventaja en django es que no tenemos que hacernos cargo de la ruta. Por ejemplo, el parámetro "lookup_field" que es "slug_name"
    # hace que en lugar de mandar el id en la url, ej: "/localhost:8000/circles/25", el 'id' se puede reemplazar por lo que contenga
    # el campo "slug_name" (y por esto es único). Entonces quedaría: "/localhost:8000/circles/facuciencias" y con ésto habilitado
    # no se uede llamar a la url con el id porque tira error
    lookup_field = 'slug_name'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')
    filter_fields = ('verified', 'is_limited')

# pARA LA paginacion es sencillo y se agrega en setting el numero.
# Ahora para poder customizar las acciones de listar, crear u otras, se puede sobreescribir las funciones. Ejemplo para listar
# se sobreescribe "get_queryset". Para ver más métodos hay que consultar el fuente.

    def get_queryset(self):
        """Restrict list to public-only."""
        # El queryset base va a ser "Circle.objects.all()" porque queremos que "update", delete, etc, sigan siendo con éste queryset
        queryset = Circle.objects.all() # Hasta ésta instancia no se hace ninguna query. Sino que se define que de todos los circulos, haga algo...
        if self.action == 'list': # Donde se define la accion de listar es en "self.action". Aca es donde se puede
            # customizar y especializar la query
            return queryset.filter(is_public=True) # Le agrego un filtro más. Para que sólo traiga los que son "is_public"
        return queryset

# Para usar las autenticaciones ver más en la docu. El que usamos en este proyecto de ejemplo es: 'DEFAULT_AUTHENTICATION_CLASSES': ( 'rest_framework.authentication.TokenAuthentication', ),
# Y ofrece "permissions" que son una serie de clases que con un true o false responden si se puede acceder a una vista, UNA VEZ QUE EL USUARIO YA ESTA
# AUTENTICADO. 

# "get_permissions" es para definir los permisos por "actions"
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            # en el folder de 'permissions' esta el archivo 'circles' con el permiso "IsCircleAdmin" customizado
            permissions.append(IsCircleAdmin) # Los 'permissions' son una tupla
        return [permission() for permission in permissions] # se retorna la instancia 'permissions' que se recorre de la tupla 'permissions'

# Para crear (con el mixin de create), se puede sobreescribir el método "perform_create" que recibe el "serializer CircleModelSerializer"
# 
    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save() # El save nos va a regresar el círculo
        user = self.request.user # se obtiene el user
        profile = user.profile # se obtiene el perfil
        Membership.objects.create( # especifica que se cree un "membership" con los datos que se le pasa
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
