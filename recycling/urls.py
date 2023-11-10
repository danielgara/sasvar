from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('escaneo', include('image_processing.urls')),
    path('admin/', admin.site.urls),
]
