"""Circle serializers."""
# Emmedocs -> Serializers
# Los "Serializers" son contenedores que nos permiten tomar tipos de datos complejos y convertirlos a datos nativos de python y
# después poderlos usar como json, xml o a cualquier otra cosa. Son como contenedores que amoldan datos, que permite que sólo
# tome datos que cumplen con las condiciones del "Serializer", sean transformados a un TIPO de Serializer y después los pueda
# transformar a cualquier otra cosa. Son muy similares a los "Form" de Django

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle

# La estructura es de la siguiente forma:
# El "Serializer" es una clase que hereda de 'serializers.Serializer' al cual se le definen las propiedades que va a tener
# el "objeto". Y se le agregan todas las restricciones con la que se va a crear el "modelo" para la BD.

# Serializar un objeto en shell_plus:
# In [1] from cride.circle.serializers import CircleSerializer  # Se importa el serializer
# In [2] circle = Circle.objects.latest() # Se instancia el objeto. Se trae el último.
# In [3] circle # Muestra el último objeto agregado
# In [4] serializer = CircleSerializer(circle) # Se crea el serializer con "CircleSerializer" y se le pasa la instancia creada "circle"
# In [5] serializer.data # Muestra el dato

# En la shell se puede hacer la peticion con la tool "http":
# user@machine:~$ http  get localhost:8000/circles/ -b
# user@machine:~$ http  post localhost:8000/circles/ name="nombre" slug_name="slug nombre" about="hola mundo" -v

# *********************  Ejemplo anterior ****************************
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.validators import (
    UniqueValidator,
)  # Esto valida que el dato sea único


# Usando el siguiente Serializer:
class CircleSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_token = serializers.IntegreField()
    rides_offered = serializers.IntegreField()
    members_limit = serializers.IntegreField()


# A cada campo del "Serializer", se le setean las restricciones para dato
class CreateCircleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40)
    slug_name = serializers.SlugField(
        # validators: Recibe una lista con los validadores. En el ej: recibe una instancia de "UniqueValidator"
        # UniqueValidator: recibe la query "Circle.objects.all()" para que valide que el dato sea unico en el modelo
        max_length=40, validators=[UniqueValidator(queryset=Circle.objects.all())]
    )
    about = serializers.CharField(required=False)  # Este indica que no es requerido

    # Ahora crear objetos. Es decir, tomar datos, validarlos y crear el modelo, en lugar de hacer todos los pasos de @api_view(['POST'])
        # data= serializer.data
        # circle = Circle.objects.create(**data)
    # Se usan funciones que traen los serializadores (en "saving instances"), que lo que hace es convertir datos a un modelo
    # sobreescribiendo los métodos "create()" o "update()" por ejemplo.
    def create(
        self, data
    ):  # Recibe los datos ya validados. Este método se invoca desde la instancia con "save()"
        return Circle.objects.create(**data)


@api_view(["GET"])
def list_circles(request):
    circles = Circle.objects.filter(
        is_public=True
    )  # Se define que "circle" cuando haga la query, traiga los que tengan "is_public"=True
    serializer = CircleSerializer(
        circles, many=True
    )  # "CircleSerializer" recibe la instancia "circles" y con "many=True", le decimos que son multiples datos
    return Response(serializer)


@api_view(["POST"])
def create_circles(request):
    serializer = CreateCircleSerializer(
        request.data
    )  # Recibe los datos y se los manda al "Serializer". Le manda lo que venga en el "request.data"
    serializer.is_valid(
        reaise_exception=True
    )  # "is_valid" es una funcion que trae "serializer" que permite validar si está todo 'ok'
    # Sin método "create()" en "CreateCircleSerializer" van las siguientes lineas
    # data= serializer.data # Si está todo 'ok' va a recibir la respuesta en "serializer.data" y esa es la que se responde
    ## Hasta aquí "data" tiene el objeto creado, ej: {"name":"nombre", "slug_name":"slug nombre", "about":"hola mundo"}
    ## con los campos del "CreateCircleSerializer"
    ## "**data" es la forma de desempaquetar datos en python
    # circle = Circle.objects.create(**data)

    # Con método "create()" en "CreateCircleSerializer" van la siguiente linea:
    circle = (
        serializer.save()
    )  # Con "save()" se invoca el método "create()" de la clase "CreateCircleSerializer"

    return Response(CircleSerializer(circle).data)
    # El "Response" termina devolviendo el objeto serializado que se usa cuando se hace el 'get', que es el momento donde se
    # consulta la BD para traer el dato. Es decir que ahora estaría incluyendo "rides_token", "rides_offered" y "members_limit"


# ********************* Fin -  Ejemplo anterior ****************************


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer."""

    members_limit = serializers.IntegerField(
        required=False, min_value=10, max_value=32000
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""

        model = Circle
        fields = (
            "name",
            "slug_name",
            "about",
            "picture",
            "rides_offered",
            "rides_taken",
            "verified",
            "is_public",
            "is_limited",
            "members_limit",
        )
        read_only_fields = (
            "is_public",
            "verified",
            "rides_offered",
            "rides_taken",
        )

    def validate(self, data):
        """Ensure both members_limit and is_limited are present."""
        members_limit = data.get("members_limit", None)
        is_limited = data.get("is_limited", False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError(
                "If circle is limited, a member limit must be provided"
            )
        return data
