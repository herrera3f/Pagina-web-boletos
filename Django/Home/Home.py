from django.shortcuts import render
from django.shortcuts import HttpResponse
import requests 
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django import template


def obtener_aviones(request):
    
    # URL de API que devuelve los datos de los aviones
    api_url = 'http://localhost:3001/obtener-aviones'
    rut_en_sesion = request.session.get('usuario_rut')
    print(f'Rut almacenado en la sesión: {rut_en_sesion}')

    try:
        # Realiza la solicitud a la API para obtener los datos de los aviones
        response = requests.get(api_url)
        aviones = response.json() if response.status_code == 200 else []

        # Retorna los datos en formato JSON
        return JsonResponse(aviones, safe=False)
    except Exception as e:
        # Maneja los errores, por ejemplo
        print(f"Error al obtener aviones: {e}")
        return HttpResponse("Error al obtener datos de aviones", status=500)
    

def obtener_usuario(usuario_rut):
    # URL de la API para obtener información del usuario
    api_url = f'http://localhost:3001/obtener-usuario?rut={usuario_rut}'

    try:
        # Realiza la solicitud a la API para obtener los datos del usuario
        response = requests.get(api_url)
        resultado = response.json() if response.status_code == 200 else {}

        return resultado
    except Exception as e:
        # Maneja los errores, por ejemplo
        print(f"Error al obtener datos de usuario: {e}")
        return HttpResponse("Error al obtener datos de usuario", status=500)


def buscar_vuelos(request):
    # Obtener los parámetros de búsqueda desde request.GET
    Origen = request.GET.get('Origen', '')
    Destino = request.GET.get('Destino', '')
    fecha_salida = request.GET.get('Fecha_y_hora_de_salida', '')
    fecha_llegada = request.GET.get('Fecha_y_hora_de_llegada', '')
    otro_vueloid = request.POST.get('ID_Vuelos')

    # Realiza una solicitud HTTP a la API para obtener los vuelos
    url_api_node = 'http://localhost:3001/buscar-vuelos'
    params = {
        'Origen': Origen,
        'Destino': Destino,
        'Fecha_y_hora_de_salida': fecha_salida,
        'Fecha_y_hora_de_llegada': fecha_llegada,
        'Rut': request.session.get('usuario_rut'),
        'ID_Vuelos': otro_vueloid
    }

    try:
        response = requests.get(url_api_node, params=params)
        response.raise_for_status()  # excepción si la solicitud no tiene éxito

        vuelos_encontrados = response.json()
    except requests.RequestException as e:
        print(f'Error al conectarse a la API de Node.js: {e}')
        vuelos_encontrados = []
        
    #verificar que los vuelos se recibieron correctamente
    print(f'Vuelos encontrados: {vuelos_encontrados}')

    # Agrega el contexto 'usuario_rut' para que esté disponible en la plantilla
    context = {'vuelos_encontrados': vuelos_encontrados, 'usuario_rut': request.session.get('usuario_rut')}

    # Renderiza la página de resultados (resultados.html) con los vuelos encontrados
    return render(request, 'Home/resultados.html', context)

def home(request):
    return render(request, 'home/home.html', {'usuario_rut': request.session.get('usuario_rut')} )