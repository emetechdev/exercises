"""Circle membership views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from cride.circles.models import Circle, Membership, Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember

# Serializers
from cride.circles.serializers import MembershipModelSerializer, AddMemberSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle membership view set."""


    serializer_class = MembershipModelSerializer

# El primer reto es que cada vez que se esté validando la vista, el circulo debe estar disponible para toda la clase. Para eso se
# usa el método "dispatch" que es el método que se encarga de manejar todas las peticiones. Particularmente de cómo van a ser servidas.
# Pero desde aquí tambien se pueden llamar a otros métodos.
# En la docu se ve que viene de "APIView" y de "View".
# Todo esto se va  a ejecutar antes de que empiece a responder peticiones. Como hasta acá no se tiene la "query" de la define en
# "def get_queryset(self):" para decirle que tome los circulos que estén activos
    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        # Los "slug names" del circulo van a estar en los keywords arguments, que esto viene de la url "kwargs['slug_name']"
        slug_name = kwargs['slug_name']
        # "self.circle = get_object_or_404(Circle, slug_name=slug_name)" acá se dice que el objeto que se va a obtener es el circulo,
        # se le pasa el "slug_name"
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]

# "get_queryset" este método se sobreescribe para traer a todos los circulos.Porue hasta ésta instancia no los tiene.
    def get_queryset(self):
        """Return circle members."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True # Trae sólo los que están ativos
        )

# El "get_object" regresa el miembro
    def get_object(self):
        """Return the circle member by using the user's username."""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )

# "perform_destroy" Es el que hace el borrado, pero en este caso sumamos el cambio "is_active" = false
    def perform_destroy(self, instance):
        """Disable membership."""
        instance.is_active = False
        instance.save()

# Es una interfaz que a traves de la cual la BD puede ser consultadas con operaciones de querys. Los mangers se acceden a traves de la
# propiedad "object" de cada clase. Ej: Se puede hacer "Circle.object". A partir de "objetc" estamos usando el manager. Cosas como ".filter"
# ".all", ".value". Y puede ser que se necesite un propio managr asi que se puede customizar.

# En ésta accion la idea es que la vista genere todos los codigos que un usuario tenga disponible para compartir con sus amigos y los codigos
# que compartio.
# "detail=True" necesita saber de que usuario es
    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve a member's invitations breakdown.

        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't being used yet.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False
        ).values_list('code')
        # "remaining_invitations" son las invitaciones quee le quedan para compartir
        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'circle': self.circle, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)
