"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User, Profile

# Tasks
from cride.taskapp.tasks import send_confirmation_email

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt


# Las peticiones para prueba se hace: primero a signup para registrar el usuario, luego

# Ej httpie de signup: http localhost:8000/users/signup/ email=mail@mail.com password=contra1234 password_confirm=contra1234 first_name=nombre last_name=apellido username=nombreusuario phone_number=41387461823 -b
# 


# Un modelo de objeto para usarlo con los serializers. Este modelo se usa para devolver en un json en el Response. Esto se hace
# con la propiedad "is_verified" que va a responder con true o false una vez que le pasemos por parametro el email a verificar.

class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class: En ésta clase se definen los atributos de los serializers"""

        model = User # Se define el modelo
        # en "fields" se definen los campos
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        )

# una vez que tenemos el sugnup, queda limitar el login unicamente a usuarios que hay verificado su cuenta
class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())] # "UniqueValidator": Valida que el mail sea único
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data): # Se hacen las validaciones correspondientes
        """Verify passwords match."""
        # "data": es un diccionario y se setean las variables con los valores del diccionario para compararlas y validar
        passwd = data['password'] 
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        # "password_validation" es un módulo de DJ. Si "password_validatiion" falla, lanza una excepcion de DJ y es catchada por DJ de manera correcta.
        password_validation.validate_password(passwd) 
        return data

    def create(self, data):
        """Handle user and profile creation."""
        # Ahora al guardar a "user", sacamos el "password_confirmation" porque no sirve mas
        data.pop('password_confirmation') # Sacamos "password_confirmation" con un "pop"
        # "create_user" éste método es especial, no es lo mismo que el "create" a secas. "create_user" es del manager de "user", entonces
        # para crear el "user" se le pasa "**data" con los datos que va a crear el user y aunque el modelo ya tengo seteado por defecto que
        # "is_verified" va a ser falso, se le va a pasar igual el parametro "is_verified=False"
        user = User.objects.create_user(**data, is_verified=False, is_client=True)
        Profile.objects.create(user=user) # Se crea el "profine" y el retorno no lo guardamos en variable porque no hace falta devolverlo
        # Ahora para poder validar el email en el ejemplo se usa "any mail" y esta configurado en éste proyecto para su uso. Esto manda un email
        # ésta funcion está desarrollada en: /cride/taskapp/tasks.py y se le pasa el "pk" por parametro
        send_confirmation_email.delay(user_pk=user.pk)
        return user

# Del LOGIN se espera que ya para cuando se haga el login, además de validadar las credenciales, ya se hayan verificado las cuentas

# Emmedocs -> 
class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    # validate: Sirve para validar los serializers, sobreescribiendolo. Recibe la data del request
    def validate(self, data):
        """Check credentials."""
        # authenticate: viene de "contrib.auth" y recibe las credenciales. Si éstas son válidas, regresa el usuario
        user = authenticate(username=data['email'], password=data['password'])
        # En base a la validación, se devuelve una respuesta
        # Ahora, lo que se busca es: En lugar de usar el 'email', se busca usar una instancia de 'user', que ya lo tenemos. Y hacemos ésto
        # para poder regresar los datos del usuario y/o otros datos mas, segun lo que ncesite.
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified: # Aca se lanza la excepcion si la cuenta no esta verificada
            raise serializers.ValidationError('Account is not active yet :(')
        # Los "Serializers" poseen un contexto (como los templates), y el "contexto" es otro atributo de clase como cualquier clase de paython.
        # Entonces se puede hacer "self.context['user] = user". Y esto lo que va a hacer es que cuando se llama a "def create()", que se hace después
        # de llamar a "def validate()", el context ya va a existir y voy a poder acceder a "user" desde el método "def create()"
        self.context['user'] = user # self.context es un diccionario.
        return data



    # Para agregar 'tokens' hay que agregar la aplicación de DJRestFr. en el 'config' que es: INSTALLED_APPS = (... "res_framework.authentication")
    # Luego hay que hacer las 'migrations' porque DJ las agrega en texto plano.
    # Luego con "Token" se pueden usar varios métodos. Ahora éste Token no es muy seguro porque tiene una "llave" (el token), un usuario (que 
    # es a quien le pertenece el token y solo hay un token por usuario. Y esto hace que renovar la "llave" se vuelva complejo).
    # Y después tiene un método "save" que si el usuario no tiene un token, le genera la llave no muy segura. Encima los guarda en texto plano
    # ESTE CURSO ES DE ANTES DEL 2020 - HAY QUE ACTUALIZARLO!
    def create(self, data):
        """Generate or retrieve new token.""" 
        # Es retrieve porque el modelo es "one to one field" y cada token tiene un usuario y si se quiere generar un nuevo token para un usuario,
        # El modelo va a romper y va a exponer el error "ya hay un token para tal usuario"

        # Para obtener el token se usa 'get_or_create' que primero trata de obtenerlo, y si no lo obtiene, lo crea.
        # "user=self.context['user']": Aca se puede acceder al "user" que se guardó en el context en el método anterior (se lo guardó en el "def validate()").
        token, created = Token.objects.get_or_create(user=self.context['user'])
        # Entonces se retorna el user y el "token.key"
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
