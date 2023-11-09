from django.shortcuts import render


def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    return render(request, 'scanner.html', {"viewData": viewData})
