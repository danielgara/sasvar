from django.shortcuts import render


def index(request):
    viewData = {}
    viewData["breadcrumb"] = False
    return render(request, 'index.html', {"viewData": viewData})


def about(request):
    viewData = {}
    viewData["breadcrumbItems"] = [
        {"name":"Inicio", "route":"home.index"},
        {"name":"Acerca", "route":"home.about"},
    ]
    return render(request, 'about.html', {"viewData": viewData})
