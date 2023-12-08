from django.shortcuts import render
from django.conf import settings


def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner.html', {"viewData": viewData})
