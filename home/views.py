from django.shortcuts import render


def index(request):
    viewData = {}
    viewData["title"] = "SASVAR"
    viewData["breadcrumb"] = False
    return render(request, 'index.html', {"viewData": viewData})


def about(request):
    viewData = {}
    viewData["title"] = "Acerca de Nosotros"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Acerca", "route": "home.about"},
    ]
    return render(request, 'about.html', {"viewData": viewData})


def categories(request):
    viewData = {}
    viewData["title"] = "Categorías"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Categorías", "route": "home.categories"},
    ]
    return render(request, 'categories/index.html', {"viewData": viewData})


def c1(request):
    viewData = {}
    viewData["title"] = "Papel y cartón limpios"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Categorías", "route": "home.categories"},
        {"name": "Papel y cartón limpios", "route": "home.categories.c1"},
    ]
    return render(request, 'categories/paper.html', {"viewData": viewData})


def c2(request):
    viewData = {}
    viewData["title"] = "Empaques y envoltorios"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Categorías", "route": "home.categories"},
        {"name": "Empaques y envoltorios", "route": "home.categories.c2"},
    ]
    return render(request, 'categories/pack.html', {"viewData": viewData})


def c3(request):
    viewData = {}
    viewData["title"] = "Residuos no aprovechables"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Categorías", "route": "home.categories"},
        {"name": "Residuos no aprovechables", "route": "home.categories.c3"},
    ]
    return render(request, 'categories/not-usable.html', {"viewData": viewData})


def c4(request):
    viewData = {}
    viewData["title"] = "Orgánicos"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Categorías", "route": "home.categories"},
        {"name": "Orgánicos", "route": "home.categories.c4"},
    ]
    return render(request, 'categories/organic.html', {"viewData": viewData})


def experience(request):
    viewData = {}
    viewData["title"] = "Registro de Experiencia"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Registro de Experiencia", "route": "home.experience"},
    ]
    return render(request, 'experience.html', {"viewData": viewData})
