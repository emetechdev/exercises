"""Users app."""

# Django
from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    """Users app config."""

    name = 'cride.users' # nombre de la app. Acá se antepone 'cride' porque es el módulo donde se ubica.
    verbose_name = 'Users' # Esta es la forma en cómo se llama en plural.
