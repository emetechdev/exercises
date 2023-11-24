"""Membership serializers."""

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers

# Serializers
from cride.users.serializers import UserModelSerializer

# Models
from cride.circles.models import Membership, Invitation


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    # Hay diferentes maneras de relacionar campos, (hay mas info en : https://www.django-rest-framework.org/api-guide/relations/)
    # la mas comun es por primary key. Esto muestra los datos relacionados com un arreglo: 
    # "results" : [ {"user": {...}, "is_admin" ...}, {"user2": {...}, "is_admin" ...}, etc]
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'user', # Con "user = UserModelSerializer(read_only=True)" se anida un user
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at' # Com oeste campo no lo tenemos, lo definimos mas arriba en "joined_at = serializers.DateTimeField(source='created', read_only=True)"
        )
        read_only_fields = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
        )


class AddMemberSerializer(serializers.Serializer):
    """Add member serializer.

    Handle the addition of a new member to a circle.
    Circle object must be provided in the context.
    """

    invitation_code = serializers.CharField(min_length=8)
    # "HiddenField": Este metodo no valida contra la entrada del usuario, sino que lo valida de manera interna. Y se le puede agregar
    # un parametro que en el ejemplo es el user por default
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Sobreescribir "validate_user". Se toma del 'context' el circulo
    def validate_user(self, data):
        """Verify user isn't already a member."""
        circle = self.context['circle']
        # De ésta linea "user = serializers.HiddenField(default=serializers.CurrentUserDefault())" se obtiene una instancia del 
        # 'user' así que el "data" que recibe por parametro el metodo "validate_user" es el 'user'
        user = data
        q = Membership.objects.filter(circle=circle, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already member of this circle')
        return data

    def validate_invitation_code(self, data):
        """Verify code exists and that it is related to the circle."""
        try:
            invitation = Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return data

    def validate(self, data):
        """Verify circle is capable of accepting a new member."""
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle has reached its member limit :(')
        return data

    def create(self, data):
        """Create new circle member."""
        circle = self.context['circle']
        invitation = self.context['invitation']
        user = data['user']

        now = timezone.now()

        # Member creation
        member = Membership.objects.create(
            user=user, # El user es el que hace la peticion
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )

        # Update Invitation
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        # Update issuer data
        issuer = Membership.objects.get(user=invitation.issued_by, circle=circle)
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member
