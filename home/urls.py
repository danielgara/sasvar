from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('acerca', views.about, name='home.about'),
    path('aprende', views.learn, name='home.learn'),
    path('aprende/nivel-1', views.l1, name='home.learn.l1'),
    path('aprende/nivel-1/<str:name>', views.l1_sublevel, name='home.learn.l1.sublevel'),
    path('aprende/nivel-2', views.l2, name='home.learn.l2'),
    path('aprende/nivel-2/<str:name>', views.l2_sublevel, name='home.learn.l2.sublevel'),
    path('aprende/nivel-3', views.l3, name='home.learn.l3'),
    path('encuentra', views.locate, name='home.locate'),
    path('experiencia', views.experience, name='home.experience'),
]
