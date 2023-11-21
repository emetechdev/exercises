"""Users views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
    AccountVerificationSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer
)

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Generate API View es una clase que permite obtener datos dado un query set, o para usar serializers, etc. Estos atributo que permiten
# ciertos comportamientos. Y permite indicar con "serializer_class" que serializers se van a usar para listar, crear o consultar cosas etc.
# Y esto permite reducir aún más el código.
# Generate API VIew permite extender la funcionalidad de una sola clase que agrega solo métodos y atributos a funcionalidades particulares.
# Con éste concepto se rigen los "MIXINS" que son claeses que exponen métodos y éstos métodos pueden ser llamados por otras clases.
# Por ejemplo "ListModelMixin" lo que hace es listar y asi están las clases para crear, modificar, crear y listar, etc.
# Ejemplo, la "class CreateAPIView(mixins.CreateModelMixin, GenericAPIView)" lo que hace es definir que va a hacer cuando se llame con un post.
# Y si es post, va a crear, no importa que... va a crear.
# Otro ejemplo, en el fuente esta la "class RetrieveUpdateDestroyAPIView(...)" que si se le manda "get" hace un retrieve, con un "put" hace un
# "self.update", con un "patch" hace un "self.partial_update" y con el "delete" hace por supuesto un "self.delete".
# Y toda la magia viene más de las clases "Mixins" que de la "GenerateAPIView"

# Los View Sets: Se definen como un conjunto de vistas que se encargan de todas estas funcionalidades que describí para las "GenericAPIViews"
# o las de los "Mixins". Y así como con los mixins "ListModelMixin" se encarga de listar, el "create" de crear, bueno, los View sets
# se encargan directamente de todo dentro de la misma clase, porque se parece a una recopilacion de mixins.. de hecho en el fuente
# se ve que los usa.


# en el ejemplo se va a usar "class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet)"
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True) # Trae los usuarios que sean activos y que sean clientes
    serializer_class = UserModelSerializer
    lookup_field = 'username' # Esto define que en la url se va a incluir el username en el lugar del id.
    # hay mas info en el view set de circulos

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']: # En estas peticiones no pide permisos y habilita a todos con [AllowAny]
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated] # Aca pregunta si esta autenticado y esta "en sesion", si es así, devuelve la instancia del permiso
        return [p() for p in permissions]

# En la docu tambien hay View set Actions para la distintas acciones. Pero tambien se pueden crear acciones propias. Las acciones se
# dividen en dos: Las que son de detalle y las que no lo son. Las de detalle, son las que parten o usan algún "id", y las que no, no usan 
# un 'id. Para éstas acciones se usa el decorador "@action(detail=False, methods=['post'])", el post es porque solo va a recibir esa accion
# Y "detail=False" indica si la accion es de detalle o no. 
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    # La url usa el nombre del método, en éste caso es "signup", esto lo hace por defecto pero tambien esta la opcion de customizarlo
    def signup(self, request): # La url queda /users/signup
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)

# Este action si es con "detail=True" porque se espera un identificador para obtener el perfil de un usuario en especifico
    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        # 'partial' es para saber si la modificacion es parcial o no.
        # Esta nomenclatura "request.method == 'PATCH'" indica que si el método es 'PATCH', 'partial' va a ser true, sino es false
        partial = request.method == 'PATCH' 
        serializer = ProfileModelSerializer( # Se instancia el perfil
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True) # se valida el perfil
        serializer.save()
        # Este paso "data = UserModelSerializer(user).data" es para definir en el modelo de "User" un objeto "Profile"
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs): # Esto devuleve los circulos a los que pertenece el usuario
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response


# Emmedocs -> Instancia anterior al resultado final
# classy DJRestFr. (www.cdrf.co) permite analizar la herencia de clases de DJRestFr. En ésta pagina se ordenan las clases
# y se pueden consultar ascendentes y descendentes, además de los métodos y sus parámetros.
# "def dispatch" es la clase padre

# APIView: Esta hereda de la clase "View" de Django y el objeto "Request" viene de DJRestFR. Tambien agrega .get() y .post()
# from rest_framework.views import APIView 

# from cride.users.serializers import UserLoginSerializer, UserSignUpSerializer


# Esta clase se reemplaza por: @action(detail=False, methods=['post'])... def login(self, request)
# class UserLoginAPIView(APIView):
#     # Reescribimos el método .post()
#     def post(self, request, *args, **kwargs):
#         # Ahora todo ésto se puede comprimir en menos líneas y es como queda más arriba en el código que es la versión final
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # Luego para cuando le doy "save" me tendría que devolver un nuevo token. Para que lo haga, en el serializer sobreescribo el método "create"
#         user, token = serializer.save()
#         data = { # Pones así el json es mala practica porque puede ser inconsistente en caso de omitir algun parametro.
#             # Para devolver el "Modelo del Serializer" usando "UserModelSerializer", se le pasa por parámetro la instancia "user". (Esto es porque
#             # "UserModelSerializer" recibe un objeto) y con ".data" se accede a los datos.
#             'user': UserModelSerializer(user).data,
#             'access_token': token
#         }
#         return Response(data, status=status.HTTP_201_CREATED)
    


# Esta clase se reemplaza por: @action(detail=False, methods=['post'])... def signup(self, request):
# class UserSignUpAPIView(APIView):
#     # Reescribimos el método .post()
#     def post(self, request, *args, **kwargs):
#         serializer = UserSignUpSerializer(data=request.data) # El serializer va a ser "UserSignUpAPIView" y recibe el "request.data"
#         serializer.is_valid(raise_exception=True)
#         # Y acá con el "serializer.save()" tenemos que verificar la cuenta, antes de que retorne el token
#         user = serializer.save()
#         data = UserModelSerializer(user).data # Solo devuelve el "user"
#         return Response(data, status=status.HTTP_201_CREATED)
    

# Esta clase se reemplaza por: @action(detail=False, methods=['post'])... def verify(self, request):
# class AccountVerificationAPIView(APIView):
#     # Reescribimos el método .post()
#     def post(self, request, *args, **kwargs):
#         serializer = AccountVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # No vamos a obtener nada despues del "serializer.save()" asi que solo se llama el método
#         serializer.save()
#         data = {'message': 'Felicitaciones'} # Solo se muestra un mensaje de exito, no mas que eso
#         return Response(data, status=status.HTTP_200_OK)