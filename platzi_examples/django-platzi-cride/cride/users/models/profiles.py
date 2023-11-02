"""Profile model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Profile(CRideModel):
    """Profile model.

    A profile holds a user's public data like biography, picture,
    and statistics.
    """

    # Para extender el modelo de usuarios se usa "models.OneToOneField". Es decir del usuario de django, le agrego (o extiendo)
    # campos y caracteristicas nuevas. Y no se meten dentro de 'users.User' porque no son datos del 'usuario' propiamente dicho
    # sino que son datos del perfil. Entonces para organizar mejor el codigo y estructurarlo de forma correcta, se lo extiende.
    # Si se usa este campo "on_delete=models.CASCADE" se indica que cuando se borre el usuario, tambien se borra el perfil.
    # Otros usos: "on_delete=models.SET_NULL" se usa para setear a null.
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture', # Es el name
        upload_to='users/pictures/', # Ubicacion del archivo
        blank=True, # Significa que no es requerido el valor y que puede ir un blanco en éste campo "picture"
        null=True # Acepta valores nullos
    )
    
    biography = models.TextField(max_length=500, blank=True)

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=5.0,
        help_text="User's reputation based on the rides taken and offered."
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)

