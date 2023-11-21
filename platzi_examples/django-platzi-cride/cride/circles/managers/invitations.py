"""Circle invitation managers."""

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits

# Emedocs: Este manager es para gestionar las invitaciones
# Para personalizar un manager, se hereda de "models.Manager" y la clase se llama "InvitationManager"
class InvitationManager(models.Manager):
    """Invitation manager.

    Used to handle code creation.
    """

    CODE_LENGTH = 10 # Definimos que los codigos sean de 10 caracteres

# Cuando se mande a llamar "def create()" primero hay que tener un conjunto de caracteres válidos.
    def create(self, **kwargs):
        """Handle code creation."""
        pool = ascii_uppercase + digits + '.-' #Esto puede ser un pool de caraacteres
        #Luego si en los "kwargs" no viene un codigo, se va a generar uno. Entonces escogemos un caracter random del "pool".
        # "pool" va a retornar una lista de caracteres y luego se juntan con "join"
        code = kwargs.get('code', ''.join(random.choices(pool, k=self.CODE_LENGTH)))
        # Y para que no hayan problemas. la siguiente linea define que mientras "self.filter(code=code).exists():". Es decrir, mientras no haya
        # otro codigo con éste código (que yo traje de los kwargs argument o el que acabo de generar). Mientras no exista, genera un nuevo codigo

        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))
        kwargs['code'] = code
        return super(InvitationManager, self).create(**kwargs)
    # Este codigo lo que hace es validar si  el code usado no ha sido usado antes y si no esta recibiendo un code, lo genero 
    # de manera aleatoria.

# Al usar éste manager en consola tipo power_shell hay que tener una instancia de un circulo
#circulo = Circle.object.first()
# Y luego al manager se le pasa el user por "issued_by" y la instancia del circulo
#Invitation.object.create(issued_by=user, circulo)