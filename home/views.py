from django.shortcuts import render


def index(request):
    viewData = {}
    viewData["title"] = "SASVAR"
    return render(request, 'home/index.html', {"viewData": viewData})


def about(request):
    viewData = {}
    viewData["title"] = "Acerca de Nosotros"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Acerca", "route": "home.about"},
    ]
    return render(request, 'home/about.html', {"viewData": viewData})


def learn(request):
    viewData = {}
    viewData["title"] = "Aprende"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.aprende"},
    ]
    return render(request, 'home/learn/index.html', {"viewData": viewData})


def l1(request):
    viewData = {}
    viewData["title"] = "Nivel 1"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Nivel 1", "route": "home.learn.l1"},
    ]
    return render(request, 'home/learn/l1.html', {"viewData": viewData})


def l1_sublevel(request, name):
    viewData = {}
    viewData["title"] = name.capitalize()
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Nivel 1", "route": "home.learn.l1"},
        {"name": name.capitalize(), "route": "home.learn.l1.sublevel", "params": {"name": name}},
    ]
    return render(request, 'home/learn/l1/' + name + '.html', {"viewData": viewData})


def experience(request):
    viewData = {}
    viewData["title"] = "Registro de Experiencia"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Registro de Experiencia", "route": "home.experience"},
    ]
    return render(request, 'home/experience.html', {"viewData": viewData})
