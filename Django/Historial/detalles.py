# En tu archivo views.py
from django.shortcuts import render
import requests

def detalles_vuelo(request, ID_Vuelos):
    try:
        # Hacer una solicitud a tu API para obtener detalles del vuelo
        api_url_detalles_vuelo = f'http://localhost:3001/obtener-detalles-vuelo-historial?id={ID_Vuelos}'
        response_detalles_vuelo = requests.get(api_url_detalles_vuelo)
        response_detalles_vuelo.raise_for_status()  # Lanza una excepción en caso de error HTTP

        detalles_vuelo = response_detalles_vuelo.json()
        print('Detalles del vuelo obtenidos:', detalles_vuelo)


        return render(request, 'Historial/detalles_vuelo.html', {'detalles_vuelo': detalles_vuelo})
    except requests.exceptions.RequestException as e:
        # Manejar errores en la solicitud a la API
        print(f'Error al obtener detalles del vuelo desde la API: {e}')
        return render(request, 'Historial/detalles_vuelo.html', {'mensaje': 'Error al obtener detalles del vuelo'})
