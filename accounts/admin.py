from django.contrib import admin
from .models import User, Ranking, Code, UserHistory, Waste, ScanData
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin import ModelAdmin
import csv
from django.http import HttpResponse
from io import StringIO
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count

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


@admin.register(Code)
class CodeAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'created_at':
            formfield.label = 'Fecha de creación'
        elif db_field.name == 'random_code':
            formfield.label = 'Código aleatorio (8 dígitos - mayúsculas)'
        elif db_field.name == 'used_by_user':
            formfield.label = 'Utilizado por usuario'
        elif db_field.name == 'redemption_date':
            formfield.label = 'Fecha de redención'
        elif db_field.name == 'user':
            formfield.label = 'Usuario'
        return formfield

    def get_actions(self, request):
        actions = super(CodeAdmin, self).get_actions(request)
        actions['download_csv'] = (CodeAdmin.custom_download_csv, 'download_csv', 'Download CSV')
        return actions

    def custom_download_csv(modeladmin, request, queryset):
        fields = ['random_code']

        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(fields)

        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="codes.csv"'
        return response


@admin.register(UserHistory)
class UserHistoryAdmin(ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'user':
            formfield.label = 'Usuario'
        elif db_field.name == 'type_of_activity':
            formfield.label = 'Tipo de actividad'
        elif db_field.name == 'accumulated_points':
            formfield.label = 'Puntos acumulados'
        elif db_field.name == 'created_at':
            formfield.label = 'Fecha de creación'
        return formfield


@admin.register(Waste)
class WasteAdmin(ModelAdmin):
    change_list_template = 'accounts/admin/waste_list.html'

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'iteration':
            formfield.label = 'Iteración'
        elif db_field.name == 'date':
            formfield.label = 'Fecha'
        elif db_field.name == 'name_ima_before':
            formfield.label = 'Nombre imagen antes'
        elif db_field.name == 'name_ima_after':
            formfield.label = 'Nombre imagen después'
        elif db_field.name == 'mode':
            formfield.label = 'Modo'
        elif db_field.name == 'folder':
            formfield.label = 'Carpeta'
        elif db_field.name == 'res':
            formfield.label = 'Res'
        elif db_field.name == 'rec':
            formfield.label = 'Rec'
        elif db_field.name == 'ecological_point':
            formfield.label = 'Punto ecologico'
        elif db_field.name == 'model_version':
            formfield.label = 'Versión del modelo'
        elif db_field.name == 'success':
            formfield.label = 'Éxito'
        return formfield


from django.db.models import Count
from django.contrib import admin
from django.shortcuts import render
from .models import ScanData

@admin.register(ScanData)
class ScanDataAdmin(admin.ModelAdmin):
    # Configuración de visualización de la tabla
    list_display = ('id', 'waste_type', 'container', 'timestamp', 'user')
    search_fields = ('waste_type', 'container')
    list_filter = ('waste_type', 'timestamp')
    change_list_template = "accounts/admin/residuo_changelist.html"

    # Personaliza etiquetas en el formulario de administración
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'waste_type':
            formfield.label = 'Tipo de residuo'
        elif db_field.name == 'container':
            formfield.label = 'Contenedor'
        elif db_field.name == 'timestamp':
            formfield.label = 'Fecha y hora de escaneo'
        elif db_field.name == 'user':
            formfield.label = 'Usuario'
        return formfield

    # Función para mostrar gráficos y los datos en el panel de administración
    def changelist_view(self, request, extra_context=None):
        # Obtener rango de fechas de los filtros
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        queryset = self.get_queryset(request)

        # Filtrar por rango de fechas si están definidos
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        # Contar residuos por tipo para el gráfico
        data = queryset.values('waste_type').annotate(total=Count('id'))

        # Pasar los datos al contexto
        extra_context = extra_context or {}
        extra_context["data"] = data
        extra_context["start_date"] = start_date
        extra_context["end_date"] = end_date

        # Llamar a la vista original de la lista de objetos (tabla de datos)
        return super().changelist_view(request, extra_context=extra_context)

    



"""class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Administración Personalizado"
    site_title = "Admin Turisinnlab"
    index_title = "Bienvenido al Panel de Administración"

    # Registra el modelo ScanData en el sitio de administración personalizado
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('scanner-chart/', self.admin_view(self.chart_view), name='scanner_chart'),  # Página personalizada para el gráfico
        ]
        return custom_urls + urls

    def chart_view(self, request):
        return TemplateResponse(request, "admin/scanner_chart.html", {})

# Instancia de sitio de administración personalizado
custom_admin_site = CustomAdminSite(name='custom_admin')

# Registra el modelo ScanData en el sitio de administración personalizado
custom_admin_site.register(ScanData)


@admin.register(ScanData)
class ResiduoAdmin(admin.ModelAdmin):
    list_display = ('tipo_residuo', 'contenedor', 'fecha', 'usuario')
    list_filter = ('tipo_residuo', 'fecha')

    def changelist_view(self, request, extra_context=None):
        # Filtrar residuos por rango de fecha usando parámetros GET
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        queryset = self.get_queryset(request)

        if start_date and end_date:
            queryset = queryset.filter(fecha__range=[start_date, end_date])

        # Contar residuos por tipo para el gráfico
        data = queryset.values('tipo_residuo').annotate(total=Count('id'))

        extra_context = extra_context or {"data": data}
        return super().changelist_view(request, extra_context=extra_context)"""