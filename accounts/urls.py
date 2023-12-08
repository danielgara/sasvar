from django.urls import path
from . import views

urlpatterns = [
    path('cerrar-sesion', views.custom_logout, name='accounts.logout'),
    path('iniciar-sesion', views.custom_login, name='accounts.login'),
    path('registro', views.signup, name='accounts.signup'),
    path('perfil', views.profile, name='accounts.profile'),
    path('divisiones', views.rankings, name='accounts.rankings'),
    path('', views.index, name='accounts.index'),
]
