from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'scanner.html', {"viewData": viewData})
