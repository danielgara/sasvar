from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            'Campos adicionales',
            {
                'fields': (
                    'profile_picture',
                    'experience_points',
                ),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'profile_picture':
            formfield.label = 'Imagen de perfil'
        elif db_field.name == 'experience_points':
            formfield.label = 'Puntos de experiencia'
        return formfield
