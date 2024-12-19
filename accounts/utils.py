from cryptography.fernet import Fernet
from django.conf import settings
from .models import Code
import pandas as pd
from collections import defaultdict
from .models import ScanData


def decrypt_message(encrypted_message):
    key = settings.CRYPTO_KEY
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
    split_pattern = decrypted_message.split('-')
    if len(split_pattern) == 6:
        id_physical_location = split_pattern[0]
        consecutive = split_pattern[1]
        try:
            code = Code.objects.get(id_physical_location=id_physical_location, consecutive=consecutive)
            raise Exception()
        except Code.DoesNotExist:
            code = Code()
            code.id_physical_location = id_physical_location
            code.consecutive = consecutive
            code.id_container = split_pattern[2]
            code.id_model = split_pattern[3]
            code.material = split_pattern[4]
            code.success = split_pattern[5]
            return code
    else:
        raise Exception()


def calcular_probabilidades():
    # Paso 1: Extraer datos de la base de datos
    scan_data = ScanData.objects.all().order_by('timestamp')
    if not scan_data.exists():
        return {}  # No hay datos disponibles

    # Convertir a DataFrame para análisis
    data = pd.DataFrame(list(scan_data.values('timestamp', 'waste_type')))
    # Paso 2: Crear transiciones entre tipos de residuos
    transitions = defaultdict(list)
    previous_waste_type = None

    for waste_type in data['waste_type']:
        if previous_waste_type:
            transitions[previous_waste_type].append(waste_type)
        previous_waste_type = waste_type

    # Paso 3: Calcular probabilidades de transición
    transition_probabilities = {
        waste_type: pd.Series(next_types).value_counts(normalize=True).to_dict()
        for waste_type, next_types in transitions.items()
    }
    return transition_probabilities


def predecir_residuo(waste_type_actual):
    probabilities = calcular_probabilidades()

    # Verificar si hay datos para el residuo actual
    if waste_type_actual not in probabilities:
        return None  # No hay datos suficientes para predecir
    # Devolver el residuo más probable
    return max(probabilities[waste_type_actual], key=probabilities[waste_type_actual].get)
