from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

def cerrar_sesion(request):
    logout(request)
    if 'usuario_rut' in request.session:
        del request.session['usuario_rut']
    
    # Obtén el nombre de la URL de la página de inicio
    nombre_url_inicio = reverse('home')

    # Construye la URL completa de la página de inicio
    url_inicio_completa = request.build_absolute_uri(nombre_url_inicio)

    print(f'URL después de cerrar sesión: {url_inicio_completa}')

    return redirect(nombre_url_inicio)