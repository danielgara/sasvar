from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from image_processing import views as image_processingViews

urlpatterns = [
    path('', include('home.urls')),
    path('test/', image_processingViews.test),
    path('escaneo/', include('image_processing.urls')),
    path('mi-cuenta/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
