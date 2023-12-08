from django.contrib import admin
from .models import User, Ranking
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin import ModelAdmin


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


@admin.register(Ranking)
class RankingAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            formfield.label = 'Nombre'
        elif db_field.name == 'level':
            formfield.label = 'Nivel'
        elif db_field.name == 'from_points':
            formfield.label = 'Puntos iniciales'
        elif db_field.name == 'to_points':
            formfield.label = 'Puntos finales'
        elif db_field.name == 'image':
            formfield.label = 'Imagen'
        return formfield
