"""Django models utilities."""

# Django
from django.db import models

# Esta es una clase abstracta
class CRideModel(models.Model):
    """Comparte Ride base model.

    CRideModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']

# Notas:
""" Herencia usando "Proxy Models". Ejemplo para visualizarlo pero no se va a usar para el proyecto en curso.
    El objetivo de los Proxy Models es extender la funcinalidad
    Los prxs nos permite extender las funcionalidades de un modelo sin crear una nueva tabla en la base de datos. Y la diferencia
    con las clases Abstractas es que éstas exponen un molde de atributos, mientras que las proxis extienden de una ya existente y
    agregan funcionalidades o funciones de la clase.
    La herencia multitabla, se trata de que si se tiene una tabla, ej "User" y otras dos como "Student" y "Personal", donde "Student" y "Personal"
    heredan de "User", ambas se van a ver reflejadas en la base de datos como una tabla.
"""
# Student hereda de una clase abstracta
# class Student (CRideModel):
#     name=models.CharField()

    # Herencia de Clase abstracta. La clase Meta hereda del meta de la clase abstracta. En éste caso django setea el 'abstract'
    # de ésta clase como 'False' automaticamente
    # class Meta(CRideModel.Meta):
    #     db_table = 'student_role'

# Ejemplo 2
# class Person(models.Model):
#     first_name=models.CharField()
#     last_name=models.CharField()

# Si tengo una clase que hereda de "Person" y quiero extender funcionalidades, y para que en la tabla no cambie en nada y no se le agreguen 
# atributos, hay que agregar en "Meta" el parámetro 'proxy' en 'True'. Y luego agregar las funciones que se necesiten agregar
# class MyPerson(Person):
#     class Meta:
#         proxy=True # Con ésto se le dice a django que no cree una tabla de "MyPerson"
    
#     def say_hi(name):
#         pass

# MyPerson.objects.all()
# ricardo=MyPerson.objects.get(pk=1)
# ricardo.say_hi('Pablo')