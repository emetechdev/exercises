"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    # list_display: Muestra los datos que se quieren mostrar
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    # list_filter: Campos seleccionados para filtrar busqueda
    list_filter = ('is_client', 'is_staff', 'created', 'modified')

# Se suma el "profile" @admin.register(Profile) 
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    # search_fields: Campos por los cuales se puede buscar
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


admin.site.register(User, CustomUserAdmin)
