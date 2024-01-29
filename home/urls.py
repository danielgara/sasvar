from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('acerca', views.about, name='home.about'),
    path('aprende', views.learn, name='home.learn'),
    path('aprende/nivel-1', views.l1, name='home.learn.l1'),
    path('categorias/empaques-envoltorios', views.c2, name='home.categories.c2'),
    path('categorias/residuos-no-aprovechables', views.c3, name='home.categories.c3'),
    path('categorias/organicos', views.c4, name='home.categories.c4'),
    path('experiencia', views.experience, name='home.experience'),
]
