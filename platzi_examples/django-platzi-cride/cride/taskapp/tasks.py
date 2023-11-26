"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Models
from cride.users.models import User
from cride.rides.models import Ride

# Celery
from celery.decorators import task, periodic_task

# Utilities
import jwt
import time
from datetime import timedelta

# Emedocs : Para el envío de email usa el "sending" de django
# Esta funcion genera el token.
# Primero se instala la librería pyjwt ("pyjwt" es un proyecto de un tal jose padilla, el git es https://github.com/jpadilla/pyjwt. En el curso usamos esto)
# y para crear un "secreto", hacemos "jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')"
# y para decodificar mandamos "jwt.decode(encoded, settings.SECRET_KEY, algorithm='HS256')"
# Para codificar tambien se pueden agregar parametros para determinar la expiracion del token, para eso hay mas info en la docu: https://pyjwt.readthedocs.io/en/stable/
# todo esto se agrega en el payload
def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    # Aca la fecha de expiración va a ser el "timezone.now()" y a ésto se le suma los días de gracia que acá van a ser 3
    exp_date = timezone.now() + timedelta(days=3)
    # En el payload van las configuraciones del token
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()), # exp: recibe un entero
        'type': 'email_confirmation' # Esto se usa para que no cualquier token pueda ser utilizado. En éste ejemplo, el token es de
        # tipo "email_confirmation" y esto se valida cuando se valide el token recibido en el endpoint que lo recibe
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256') # Esta variable "token" queda con el formato "bytes", de la 
    # siguente forma: b'....'. Por eso cuando se lo retorna, ANTES se usa el método ".decode" de python para convertirlo de formato "bytes" a "string"
    return token.decode() # ESTE "decode" NO ES EL DE JWT

# Para decirle a "Celery" que éstas son tareas de Celery se usa el decorados "@task" al cual se le pasa el nombre de la funcion
# Si la tarea viene fallando, se le puede asignar un numero máximo de veces que puede fallar y eso se hace con "max_retries", que en éste caso es 3
# Tambien se pueden agregar mas cosas pero eso es mejor consultar la docu.
@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk): 
    # Una de las buenas prácticas de "Celery" es no estar mandando datos complejos en la función, ej: "send_confirmation_email(dato_complejo)"
    # esto es porque pueden ir mutando durante su trayecto y es por eso que es mejor mandar un id por ejemplo: "send_confirmation_email(user_pk)"
# Esta función además de mandar un email, genera un token único y despues se puede validar mas abajo
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk) # Validacin de usuario por id
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    # "render_to_string" esto se manda en texto plano en caso de que no se llegara a renderizar link en el email. En el ejemplo vemos
    # el choclo del token pero para el usuario vamos a mostrar solo un botoncito lindo que oculte todo.
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()

# "@periodic_task" se usa para definir una tarea periodica en celery y se le pasa por parametro el nombre de la funcion, entre otros parametros
# "run_every=timedelta(minutes=20)" sirve para indicar cada cuanto se quiere que corra
@periodic_task(name='disable_finished_rides', run_every=timedelta(minutes=20)) # Se ejecuta cada 20 minutos
def disable_finished_rides():
    """Disable finished rides."""
    now = timezone.now()
    offset = now + timedelta(minutes=20)

    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=False)
