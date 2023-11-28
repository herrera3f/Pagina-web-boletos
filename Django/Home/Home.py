from django.shortcuts import render
from django.shortcuts import HttpResponse
import requests 
from django.shortcuts import HttpResponse
from django.http import JsonResponse

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


def buscar_vuelos(request):
    # Obtener los parámetros de búsqueda desde request.GET
    Origen = request.GET.get('Origen', '')
    Destino = request.GET.get('Destino', '')
    fecha_salida = request.GET.get('fechaSalida', '')
    fecha_llegada = request.GET.get('fechaLlegada', '')
    vueloid = request.POST.get('ID_Vuelos')



    # Realiza una solicitud HTTP a tu API de Node.js para obtener los vuelos
    url_api_node = 'http://localhost:3001/buscar-vuelos' 
    params = {'Origen': Origen, 'Destino': Destino, 'Fecha_y_hora_de_salida': fecha_salida, 'Fecha_y_hora_de_llegada': fecha_llegada, 'Rut': request.session.get('usuario_rut'), 'ID_Vuelos': vueloid}

    try:
        response = requests.get(url_api_node, params=params)
        response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito

        vuelos_encontrados = response.json()
    except requests.RequestException as e:
        print(f'Error al conectarse a la API de Node.js: {e}')
        vuelos_encontrados = []

    # Renderiza la página de resultados (resultados.html) con los vuelos encontrados
    return render(request, 'Home/resultados.html', {'vuelos_encontrados': vuelos_encontrados})

def home(request):
    return render(request, 'home/home.html')