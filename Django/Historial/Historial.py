from django.shortcuts import render
from django.http import JsonResponse
import requests
import logging

def historial_reservas(request):
    # Obtener Rut del usuario desde la sesión
    usuario_rut = request.session.get('usuario_rut')

    # Verificar si el usuario está autenticado
    if not usuario_rut:
        # El usuario no está autenticado, manejar según sea necesario
        return render(request, 'Historial/error.html', {'mensaje': 'Usuario no autenticado'})

    # Hacer una solicitud a tu API para obtener el usuario
    api_url_obtener_usuario = 'http://localhost:3001/obtener-usuario'
    params_obtener_usuario = {'rut': usuario_rut}

    try:
        response_usuario = requests.get(api_url_obtener_usuario, params=params_obtener_usuario)
        response_usuario.raise_for_status()  # Lanza una excepción en caso de error HTTP

        usuario = response_usuario.json()

        # Hacer una solicitud a tu API para obtener el historial de reservas del usuario
        api_url_historial_reservas = 'http://localhost:3001/obtener-historial-reservas'
        params_historial_reservas = {'rut': usuario_rut}

        response_historial_reservas = requests.get(api_url_historial_reservas, params=params_historial_reservas)
        response_historial_reservas.raise_for_status()  # Lanza una excepción en caso de error HTTP

        historial_reservas = response_historial_reservas.json()

        # Imprime o registra información para depuración
        print(f'Usuario: {usuario}')
        print(f'Historial de Reservas: {historial_reservas}')

        # Pasar las reservas a la plantilla
        return render(request, 'Historial/historial_reservas.html', {'usuario': usuario, 'historial_reservas': historial_reservas, 'usuario_rut': usuario_rut})
    except requests.exceptions.RequestException as e:
        # Manejar errores en la solicitud a la API
        print(f'Error al obtener usuario o historial de reservas desde la API: {e}')
        return render(request, 'Historial/error.html', {'mensaje': 'Error al obtener datos desde la API'})
