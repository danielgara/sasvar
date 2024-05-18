from django.shortcuts import render
from django.conf import settings


def index(request):
    viewData = {}
    viewData["title"] = "SASVAR"
    return render(request, 'app_test/index.html', {"viewData": viewData})


def learn(request):
    viewData = {}
    viewData["title"] = "Aprende"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.aprende"},
    ]
    return render(request, 'app_test/learn/index.html', {"viewData": viewData})


def l1(request):
    viewData = {}
    viewData["title"] = "Nivel 1"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.learn"},
        {"name": "Nivel 1", "route": "app_test.learn.l1"},
    ]
    return render(request, 'app_test/learn/l1.html', {"viewData": viewData})


def l2(request):
    viewData = {}
    viewData["title"] = "Nivel 2"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.learn"},
        {"name": "Nivel 2", "route": "app_test.learn.l2"},
    ]
    return render(request, 'app_test/learn/l2.html', {"viewData": viewData})


def l3(request):
    viewData = {}
    viewData["title"] = "Nivel 3"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.learn"},
        {"name": "Nivel 3", "route": "app_test.learn.l3"},
    ]
    return render(request, 'app_test/learn/l3.html', {"viewData": viewData})


def l1_sublevel(request, name):
    viewData = {}
    viewData["title"] = name.capitalize()
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.learn"},
        {"name": "Nivel 1", "route": "app_test.learn.l1"},
        {"name": name.capitalize(), "route": "app_test.learn.l1.sublevel", "params": {"name": name}},
    ]
    return render(request, 'app_test/learn/l1/' + name + '.html', {"viewData": viewData})


def l2_sublevel(request, name):
    viewData = {}
    viewData["title"] = name.capitalize()
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Aprende", "route": "app_test.learn"},
        {"name": "Nivel 2", "route": "app_test.learn.l2"},
        {"name": name.capitalize(), "route": "app_test.learn.l2.sublevel", "params": {"name": name}},
    ]
    return render(request, 'app_test/learn/l2/' + name + '.html', {"viewData": viewData})


def scanner(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "app_test.index"},
        {"name": "Escaneo", "route": "app_test.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'app_test/scanner.html', {"viewData": viewData})
