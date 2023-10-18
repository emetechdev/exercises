""" User model.

"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel

# AbstractUser: Hereda de otras clases como 'PermissionMixin' entre otras que son Base.
# CRideModel. Solo aporta fecha de creacion y modificacion
class User(CRideModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        'email address', # Este es el name del campo
        unique=True, # Indica que sea un campo único. No puede haber otro usuario con éste valor
        error_messages={ # Mensaje de error
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], # Validacion del input. Antes de que se guarde el valor, se valida el dato y si está bien, lo guarda.
        max_length=17, # Maximo de caracteres permitidos
        blank=True # Indica que se puede obviar este campo
        )

    USERNAME_FIELD = 'email' # Se define el 'email' como 'username' para login
    # REQUIRED_FIELDS: Campos requeridos. 'username', 'first_name' y 'last_name' sólo se nombran como requeridos pero no se declaran dentro
    # de la class 'User' porque 'estos campos ya se heredan del 'AbtractUser'. Tambien ya vienen incluidos 'is_staf', etc.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] 

    is_client = models.BooleanField(
        'client', # Name
        default=True, # Por default todos los usuarios son 'clients'
        help_text=( # Campo auxiliar que aporta texto de ayuda
            'Help easily distinguish users and perform queries. '
            'Clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )

    def __str__(self): # Esta es la definicion de 'string'. Que regresa el 'username'
        """Return username."""
        return self.username

    def get_short_name(self): # get_short_name: Por default (Si se consulta el fuente), devuelve el 'first_name'. Pero para
                              # el ejemplo se lo sobreescribe para que retorne el 'username'
        """Return username."""
        return self.username
