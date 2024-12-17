from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import json
import datetime
import random
import string
import base64
from accounts.models import ScanData


def index(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner.html', {"viewData": viewData})


def test(request):
    viewData = {}
    viewData["title"] = "Escaneo"
    viewData["breadcrumbItems"] = [
        {"name": "Inicio", "route": "home.index"},
        {"name": "Escaneo", "route": "scanner.index"},
    ]
    viewData["api_key"] = settings.API_KEY
    viewData["ip_server"] = settings.IP_SERVER
    return render(request, 'image_processing/scanner_test.html', {"viewData": viewData})


def save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data['frame']
        waste_type = data.get('waste_type', 'Desconocido')
        container = data.get('container', 'Desconocido')

        base64_str = image_data.split(";base64,")[1]
        image_data_decoded = base64.b64decode(base64_str)
        fs = FileSystemStorage()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        random_text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        file_name = f"{current_date}-{random_text}.png"
        fs.save('scanned_pics/' + file_name, ContentFile(image_data_decoded))

        # Guardar los datos de residuo y contenedor en la base de datos
        scan_data = ScanData(
            waste_type=waste_type,
            container=container,
            user=request.user if request.user.is_authenticated else None
        )
        scan_data.save()

        return JsonResponse({'status': 'success', 'message': 'Datos e imagen guardados correctamente'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
