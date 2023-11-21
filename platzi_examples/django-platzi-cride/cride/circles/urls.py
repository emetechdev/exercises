"""Circles URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views --> Se importan los views
from .views import circles as circle_views
from .views import memberships as membership_views

# Los "router" reciben un "view set", (porque saben trabajar con los view set) y es el que genera los "paths" que se necesitan
router = DefaultRouter() # se instancia "DefaultRouter", que tiene como método el "register" que recibe el "path" que es "r'circles'",
# despues recibe el "viewSET" y un nombre base
router.register(r'circles', circle_views.CircleViewSet, basename='circle')
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/members', # aca usa una expresion regular para no admitir 'slug names' que no correspondan
    membership_views.MembershipViewSet,
    basename='membership'
)

# Y como todos los módulos de url tienen que exponer una variable "urlpatterns" se le aagrega que "el path normal que es '', 
# incluye las url del 'router' que es router.urls"
urlpatterns = [
    path('', include(router.urls))
]
