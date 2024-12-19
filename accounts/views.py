from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from .forms import UserCreateForm
from .models import User, Ranking, UserHistory, Waste, ScanData
from django.db import IntegrityError
from .utils import decrypt_message
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.core.exceptions import ValidationError
from .utils import predecir_residuo


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
            return render(request, 'accounts/login.html', {"viewData": viewData})
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
    viewData["user_ranking_image"] = user_ranking.image
    viewData["user_pending_points"] = pending_points
    viewData["user_progress_percentage"] = round(progress_percentage)

    return render(request, 'accounts/rankings.html', {"viewData": viewData})


@login_required
def redemption(request, encrypted_message):
    viewData = {}
    viewData["title"] = "Redención de puntos"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Redención de puntos", "route": "accounts.redemption"},
    ]

    try:
        code = decrypt_message(encrypted_message)
        code.user = request.user
        code.save()

        gained_points = 1

        if (code.success == "1"):
            gained_points = 5

        UserHistory.objects.create(
            type_of_activity='QR_SCAN',
            accumulated_points=gained_points,
            user=request.user
        )

        request.user.experience_points += gained_points
        request.user.save()

        viewData["gained_points"] = gained_points
        viewData["success"] = "El código ha sido redimido con éxito."
    except:
        viewData["error"] = "Código inválido."

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


@login_required
def upload_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)
            print(data)
            for item in data:
                Waste.objects.create(
                    iteration=item[0],
                    date=datetime.strptime(item[1], '%d/%m/%Y/%H:%M:%S').strftime('%Y-%m-%d'),
                    name_ima_before=item[2],
                    name_ima_after=item[3],
                    mode=item[4],
                    folder=item[5],
                    res=item[6],
                    rec=item[7],
                    ecological_point=item[8],
                    model_version=item[9],
                    success=item[10]
                )
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except json.JSONDecodeError:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


def get_scan_data(request):
    # Obtener y validar las fechas del rango
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = timezone.now() - timedelta(days=7)  # Por defecto, hace una semana

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()  # Por defecto, hoy

        # Filtrar datos por el rango de fechas
        data = ScanData.objects.filter(timestamp__date__range=[start_date, end_date])

        # Escaneos por fecha
        date_data = data.annotate(date=TruncDate('timestamp')).values('date').annotate(total=Count('id')).order_by('date')
        date_labels = [entry['date'].strftime('%Y-%m-%d') for entry in date_data]
        date_values = [entry['total'] for entry in date_data]

        # Escaneos por día y tipo de residuo
        waste_type_data = data.values('timestamp__date', 'waste_type').annotate(total=Count('id')).order_by('timestamp__date')
        waste_type_labels = list(data.values_list('waste_type', flat=True).distinct())  # Etiquetas de tipos de residuos
        final_dates = sorted({entry['timestamp__date'].strftime('%Y-%m-%d') for entry in waste_type_data})

        # Formato de datos para cada tipo de residuo
        final_data = {waste_type: [0] * len(final_dates) for waste_type in waste_type_labels}
        for entry in waste_type_data:
            date_index = final_dates.index(entry['timestamp__date'].strftime('%Y-%m-%d'))
            final_data[entry['waste_type']][date_index] = entry['total']

        return JsonResponse({
            'date_labels': date_labels,
            'date_values': date_values,
            'waste_type_labels': waste_type_labels,
            'final_dates': final_dates,
            'final_data': final_data
        })
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)


@login_required
def scanner_chart(request):
    viewData = {}
    viewData["title"] = "Gráfico del Escáner"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Mi Cuenta", "route": "accounts.index"},
        {"name": "Gráfico del Escáner", "route": "accounts.scanner_chart"},
    ]
    return render(request, 'accounts/scanner_chart.html', {"viewData": viewData})


def prediccion_residuo(request):
    # Obtener el residuo actual desde los parámetros de consulta
    waste_type_actual = request.GET.get('waste_type', None)
    if not waste_type_actual:
        return JsonResponse({'error': 'Se requiere un tipo de residuo actual'}, status=400)

    # Realizar la predicción
    siguiente_residuo = predecir_residuo(waste_type_actual)
    if siguiente_residuo:
        return JsonResponse({'siguiente_residuo': siguiente_residuo})
    else:
        return JsonResponse({'mensaje': 'No hay suficientes datos para predecir el siguiente residuo'})


def get_user_scan_data(request):
    # Obtener el usuario logueado
    user = request.user

    # Obtener y validar las fechas del rango
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        # Convertir cadenas de fecha a objetos datetime o usar valores predeterminados
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = timezone.now() - timedelta(days=7)  # Por defecto, hace una semana

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = timezone.now()  # Por defecto, hoy

        # Filtrar datos por el rango de fechas y por el usuario logueado
        data = ScanData.objects.filter(user=user, timestamp__date__range=[start_date, end_date])

        # Escaneos por fecha para el usuario
        date_data = data.annotate(date=TruncDate('timestamp')).values('date').annotate(total=Count('id')).order_by('date')
        date_labels = [entry['date'].strftime('%Y-%m-%d') for entry in date_data]
        date_values = [entry['total'] for entry in date_data]

        # Escaneos por tipo de residuo y fecha para el usuario
        waste_type_data = data.values('timestamp__date', 'waste_type').annotate(total=Count('id')).order_by('timestamp__date')
        waste_type_labels = list(data.values_list('waste_type', flat=True).distinct())  # Etiquetas de tipos de residuos
        final_dates = sorted({entry['timestamp__date'].strftime('%Y-%m-%d') for entry in waste_type_data})

        # Formato de datos para cada tipo de residuo
        final_data = {waste_type: [0] * len(final_dates) for waste_type in waste_type_labels}
        for entry in waste_type_data:
            date_index = final_dates.index(entry['timestamp__date'].strftime('%Y-%m-%d'))
            final_data[entry['waste_type']][date_index] = entry['total']

        # Respuesta en JSON
        return JsonResponse({
            'date_labels': date_labels,
            'date_values': date_values,
            'waste_type_labels': waste_type_labels,
            'final_dates': final_dates,
            'final_data': final_data
        })

    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
