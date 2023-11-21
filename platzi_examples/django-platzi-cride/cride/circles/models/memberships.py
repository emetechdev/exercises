"""Membership model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

# Emedocs
# La relación de "membresia" usa el tipo de relación que proporciona django que se llama "many to many fields". Que puede traducirse a
# una relacion muchos a muchos. Entonces, "Membership" es un modelo intermedio que relaciona y guarda datos adicionales. Hereda de "CRideModel".
# Ahora en la clase "class Circle(CRideModel):" hay que agregar "members = models.ManyToManyField('users.User', through='circles.Membership', through_fields=('circle', 'user') )"
# Para que esten los modelos con las referencias ya declaradas
class Membership(CRideModel):
    """Membership model.

    A membership is the table that holds the relationship between
    a user and a circle.
    """
    # Tiene una clave foranea que con la propiedad "on_delete" indica que cuando se borre el círculo, se borra todo. Esta condicion indica
    # que va a pasar con los datos cuando los datos donde está la "pk" se borren
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text="Circle admins can update the circle's data and manage its members."
    )

    # Invitations
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL, # No borraría a otro usuario por invitarte 
        related_name='invited_by'
    )

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active users are allowed to interact in the circle.'
    )

    def __str__(self):
        """Return username and circle."""
        return '@{} at #{}'.format(
            self.user.username,
            self.circle.slug_name
        )
