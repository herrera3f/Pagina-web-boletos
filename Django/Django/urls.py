from django.contrib import admin
from django.urls import path
from login import views, views2
from Home import Home
from Home.Home import buscar_vuelos
from Reserva import Reserva
from Historial import Historial
from Historial.detalles import detalles_vuelo
from login import cerrar_session




urlpatterns = [
    path('admin/', admin.site.urls),
    path('iniciar_sesion/', views2.iniciar_sesion, name='iniciar_sesion'),
    path('registro_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar_sesion/', cerrar_session.cerrar_sesion, name='cerrar_sesion'),
    path('', Home.home, name='home'),
    path('obtener-aviones', Home.obtener_aviones, name='obtener_aviones'),
    path('buscar-vuelos/', buscar_vuelos, name='buscar_vuelos'),
    path('reserva/', Reserva.reserva, name='reserva'),
    path('historial_reservas/', Historial.historial_reservas, name='historial_reservas'),  
    path('detalles_vuelo/<str:ID_Vuelos>/', detalles_vuelo, name='detalles_vuelo'),
]