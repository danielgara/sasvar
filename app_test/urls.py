from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanner, name='app_test.index'),
    path('aprende', views.learn, name='app_test.learn'),
    path('aprende/nivel-1', views.l1, name='app_test.learn.l1'),
    path('aprende/nivel-1/<str:name>', views.l1_sublevel, name='app_test.learn.l1.sublevel'),
    path('aprende/nivel-2', views.l2, name='app_test.learn.l2'),
    path('aprende/nivel-2/<str:name>', views.l2_sublevel, name='app_test.learn.l2.sublevel'),
    path('aprende/nivel-3', views.l3, name='app_test.learn.l3'),
]
