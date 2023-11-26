"""Invitations tests."""
# Django integra una clase a un conjunto de pruebas y hace que todas éstas pruebas sean encontradas y sean ejecutadas.
# Unitest: es un módulo de python, donde hay una clase que se llama "TestCase" que se puede usar como clase base y a partir de ella
# customizar las clases que se necesiten. Los métodos que trae "TestCase" son los que se ejecutan como pruebas.
# Y la manera de hacer pruebas es llamar al método "assertEqual()" que es uno de los múltiples métodos que python tiene para asegurarnos
# que las pruebas pasen. Cuando las pruebas no pasan, lanza una excepción y el mismo módulo de "TestCase" sabe como manejar esa excepción
# En la docu esta la lista de "asserts".

# Hay distintos tipos de pruebas. 
# - Las Pruebas Unitarias: Son las que pruebas modulos particulares y que por si solos no reflejan funcionalidades complejas
# - Pruebas de integracion: Son modulos que se componene de multiples partes o unidades.

# Django por default incluye un server de prueba llamado "live server" pero para DJRest Fr. hay una librerría que permite simular
# peticiones que se llama "APIClient" y los que nos interesa con los "APITestCase" que nos permite hacer uso de "APIClient"
# que nos permite hacer peticiones sin tener que instanciarlas y configurarlas.

# Ver "Factory Boy" libreria para testing

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from cride.circles.models import Circle, Invitation, Membership
from cride.users.models import User, Profile
from rest_framework.authtoken.models import Token


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""
# Queremos que cada una de las pruebas inice con datos sin necesidad de estar metiendo datos a cada rato. Así que se crea un usuario
# ej. 'Pablo'. Despues se crea el 'circulo'.
#
    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Pablo',
            last_name='Trinidad',
            email='pablotrinidad@ciencias.unam.mx',
            username='pablotrinidad',
            password='admin123'
        )
        self.circle = Circle.objects.create(
            name='Facultad de Ciencias',
            slug_name='fciencias',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )

# Aca se define como se va a llamar la prueba "test_code_generation()". Y se crea una nueva invitacion donde se le pasa
# el usuario y el circulo creado
    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given, there's no need to create a new one."""
        code = 'holamundo'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )

        self.assertNotEqual(code, invitation.code)


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitation API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create( # Se crea el usuario
            first_name='Pablo',
            last_name='Trinidad',
            email='pablotrinidad@ciencias.unam.mx',
            username='pablotrinidad',
            password='admin123'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create( # Se crea el circulo
            name='Facultad de Ciencias',
            slug_name='fciencias',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )
        self.membership = Membership.objects.create( # Se crea la membresia
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth: Para hacer los test se necesitan hacer las autenticaciones
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token)) # Acá se provee al usuario con las credenciales

        # URL: Se define la url
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )

# Se definene los casos de prueba. Cada funcionalidad es un caso de prueba
    def test_response_success(self):
        """Verify request succeed."""

        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitation are generated if none exist previously."""
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations URL
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations were created
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
