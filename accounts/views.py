from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect


@login_required
def custom_logout(request):
    logout(request)
    return redirect('home.index')


def custom_login(request):
    viewData = {}
    viewData["title"] = "Iniciar Sesión"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Iniciar Sesión", "route": "accounts.login"},
    ]
    if request.method == 'GET':
        return render(request, 'login.html', {"viewData": viewData})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            viewData["error"] = 'El nombre de usuario o la contraseña no son correctos.'
            return render(request, 'login.html', {"viewData": viewData})
        else:
            login(request, user)
            return redirect('home.index')
