from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from .forms import UserCreateForm
from .models import User, Ranking
from django.db import IntegrityError


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
        return render(request, 'accounts/login.html', {"viewData": viewData})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            viewData["error"] = 'El nombre de usuario o la contraseña no son correctos.'
            return render(request, 'login.html', {"viewData": viewData})
        else:
            login(request, user)
            return redirect('home.index')


def signup(request):
    viewData = {}
    viewData["title"] = "Registro"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Registro", "route": "accounts.signup"},
    ]

    if request.method == 'GET':
        viewData["form"] = UserCreateForm()
        return render(request, 'accounts/signup.html', {"viewData": viewData})
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    experience_points=0
                )
                user.save()
                login(request, user)
                return redirect('home.index')
            except IntegrityError as error:
                viewData["error"] = [error]
        else:
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(error)

            viewData["error"] = error_list

        viewData["form"] = form
        return render(request, 'accounts/signup.html', {"viewData": viewData})


@login_required
def profile(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        request.user.profile_picture = request.FILES.get('profile_pic')
        request.user.save()
        return redirect('accounts.profile')

    viewData = {}
    viewData["title"] = "Perfil"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Perfil", "route": "accounts.profile"},
    ]
    viewData["user"] = request.user
    user_points = request.user.experience_points
    user_ranking = Ranking.objects.filter(from_points__lte=user_points, to_points__gte=user_points).first()
    viewData["ranking"] = user_ranking
    return render(request, 'accounts/profile.html', {"viewData": viewData})


@login_required
def index(request):
    viewData = {}
    viewData["title"] = "Mi cuenta"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
    ]
    return render(request, 'accounts/index.html', {"viewData": viewData})


@login_required
def rankings(request):
    viewData = {}
    viewData["title"] = "Divisiones"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Divisiones", "route": "accounts.rankings"},
    ]
    viewData["rankings"] = Ranking.objects.order_by('-level')
    user_points = request.user.experience_points
    user_ranking = Ranking.objects.filter(from_points__lte=user_points, to_points__gte=user_points).first()
    viewData["user_ranking_name"] = user_ranking.name

    return render(request, 'accounts/rankings.html', {"viewData": viewData})
