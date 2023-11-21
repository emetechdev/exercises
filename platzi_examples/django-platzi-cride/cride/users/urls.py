"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

# La explicacion del 'router' esta en el modulo de url de circulos
router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]

# # Emmedocs -> Instancia anterior al resultado final
# from cride.circles.views import UserLoginAPIView, UserSignUpAPIView, AccountVerificationAPIView

# Este urlpatterns es reemplazado porque se implemento el uso de los serializers y el router es el que los maneja
# urlpatterns = [
#     path('users/login/', UserLoginAPIView.as_view(), name='login'),
#     path('users/signup/', UserSignUpAPIView.as_view(), name='signup'), # Para el ejemplo de "UserSignUpAPIView"
#     path('users/verify/', AccountVerificationAPIView.as_view(), name='verify'),
# ]