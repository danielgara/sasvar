from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from .forms import UserCreateForm
from .models import User, Ranking, Code, UserHistory
from django.db import IntegrityError
from datetime import datetime


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
            next_route = request.GET.get('next')
            if next_route:
                try:
                    return redirect(next_route)
                except:
                    pass
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
    pending_points = (user_ranking.to_points - user_points) + 1
    progress_percentage = 100 * (1 - (pending_points / (user_ranking.to_points + 1 - user_ranking.from_points)))
    viewData["user_points"] = user_points
    viewData["user_ranking_name"] = user_ranking.name
    viewData["user_pending_points"] = pending_points
    viewData["user_progress_percentage"] = round(progress_percentage)

    return render(request, 'accounts/rankings.html', {"viewData": viewData})


@login_required
def redemption(request, entered_code):
    viewData = {}
    viewData["title"] = "Redención de puntos"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Redención de puntos", "route": "accounts.redemption"},
    ]

    try:
        code = Code.objects.get(random_code=entered_code)
        if code.used_by_user:
            viewData["error"] = "El código ya ha sido redimido previamente."
        else:
            code.used_by_user = True
            code.user = request.user
            code.redemption_date = datetime.now()
            code.save()

            UserHistory.objects.create(
                type_of_activity='QR_SCAN',
                accumulated_points=5,
                user=request.user
            )

            request.user.experience_points += 5
            request.user.save()
            viewData["success"] = "El código ha sido redimido con éxito."
    except Code.DoesNotExist:
        viewData["error"] = "El código no existe."

    return render(request, 'accounts/redemption.html', {"viewData": viewData})


@login_required
def stats(request):
    viewData = {}
    viewData["title"] = "Mis estadísticas"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Estadísticas", "route": "accounts.stats"},
    ]
    viewData["user_history_entries"] = UserHistory.objects.filter(user=request.user)
    return render(request, 'accounts/stats.html', {"viewData": viewData})
