from django.shortcuts import render
from accounts.models import Ranking


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
    viewData["title"] = "Módulo 1"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Módulo 1", "route": "home.learn.l1"},
    ]
    return render(request, 'home/learn/l1.html', {"viewData": viewData})


def l2(request):
    viewData = {}
    viewData["title"] = "Módulo 2"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Módulo 2", "route": "home.learn.l2"},
    ]
    return render(request, 'home/learn/l2.html', {"viewData": viewData})


def l3(request):
    viewData = {}
    viewData["title"] = "Módulo 3"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Módulo 3", "route": "home.learn.l3"},
    ]
    return render(request, 'home/learn/l3.html', {"viewData": viewData})


def l1_sublevel(request, name):
    viewData = {}
    viewData["title"] = name.capitalize()
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Módulo 1", "route": "home.learn.l1"},
        {"name": name.capitalize(), "route": "home.learn.l1.sublevel", "params": {"name": name}},
    ]
    return render(request, 'home/learn/l1/' + name + '.html', {"viewData": viewData})


def l2_sublevel(request, name):
    viewData = {}
    viewData["title"] = name.capitalize()
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Aprende", "route": "home.learn"},
        {"name": "Módulo 2", "route": "home.learn.l2"},
        {"name": name.capitalize(), "route": "home.learn.l2.sublevel", "params": {"name": name}},
    ]
    return render(request, 'home/learn/l2/' + name + '.html', {"viewData": viewData})


def locate(request):
    viewData = {}
    viewData["title"] = "Encuentra un Punto Ecológico"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Encuentra un Punto Ecológico", "route": "home.locate"},
    ]
    return render(request, 'home/locate.html', {"viewData": viewData})


def experience(request):
    viewData = {}
    viewData["title"] = "Registro de Experiencia"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Acumula", "route": "home.experience"},
    ]
    viewData["rankings"] = Ranking.objects.order_by('-level')
    return render(request, 'home/experience.html', {"viewData": viewData})
