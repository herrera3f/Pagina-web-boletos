from django.shortcuts import render
import pika
import json
from django.conf import settings
from django.http import HttpResponseRedirect
from Reserva.email import enviar_correo_reserva
import requests

def enviar_comando_a_rabbitmq(comando):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USERNAME,
                settings.RABBITMQ_PASSWORD,
            ),
        ))
        channel = connection.channel()

        exchange_name = 'escritura_exchange'

        # Declara el intercambio si no existe
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

        # Publica el mensaje en la cola
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='escritura',
            body=json.dumps(comando),
        )

        connection.close()
    except Exception as e:
        print(f'Error al enviar el comando a RabbitMQ: {e}')

def generar_voucher(request, reserva_info):
    # Renderiza la vista del voucher con la información de la reserva
    return render(request, 'Reserva/voucher.html', {
        'nombre_apellido': reserva_info.get('nombre_apellido', 'Desconocido'),
        'pais': reserva_info.get('pais', ''),
        'numero_documento': reserva_info.get('Numero de Documento', ''),
        'fecha_nacimiento': reserva_info.get('Fecha de Nacimiento', ''),
        'sexo': reserva_info.get('sexo', ''),
        'email': reserva_info.get('email', ''),
        'telefono': reserva_info.get('telefono', ''),
        # Agrega más detalles según sea necesario
    })




def reserva(request):
    # Obtener Rut del usuario desde la sesión
    usuario_rut = request.session.get('usuario_rut')

    # Verificar si el usuario está autenticado
    if not usuario_rut:
        # El usuario no está autenticado, manejar según sea necesario
        return render(request, 'Reserva/error.html', {'mensaje': 'Usuario no autenticado'})

    if request.method == 'POST':
        try:
            vueloid = request.POST.get('ID_vuelo')
            nombre_apellido = request.POST.get('Nombre_Apellido')
            pais = request.POST.get('Pais')
            documento = request.POST.get('Numero_de_Documento')
            nacimiento = request.POST.get('Fecha_de_Nacimiento')
            sexo = request.POST.get('Sexo')
            email = request.POST.get('Email')
            telefono = request.POST.get('Telefono')
            
            # Otros datos...
            otro_vueloid = request.POST.get('ID_Vuelos')
            api_url = f'http://localhost:3001/obtener-detalles-vuelo-id?id={otro_vueloid}'
            # Reemplaza con la URL real de tu API
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                vuelo = response.json()
            except requests.exceptions.RequestException as e:
                print(f'Error al obtener la información del vuelo desde la API: {e}')
                vuelo = None
            # Crear comandos para MySQL y MongoDB con el Rut del usuario
            comando_mysql = {
                'ID_Cliente': usuario_rut,
                'ID_Vuelos': otro_vueloid,
                'Nombre_Apellido': nombre_apellido,
                'Pais': pais,
                'Numero_de_Documento': documento,
                'Fecha_de_Nacimiento': nacimiento,
                'Sexo': sexo,
                'Email': email,
                'Telefono': telefono,
                'operacion': 'mysql_reserva',
            }

            comando_mongodb = {
                'usuario_rut': usuario_rut,
                'ID_Vuelos': otro_vueloid,  # Asegúrate de usar el valor correcto
                'Nombre_Apellido': nombre_apellido,
                'Pais': pais,
                'Numero_de_Documento': documento,
                'Fecha_de_Nacimiento': nacimiento,
                'Sexo': sexo,
                'Email': email,
                'Telefono': telefono,
                'operacion': 'mongodb_reserva',
            }

            # Enviar comandos a RabbitMQ
            enviar_comando_a_rabbitmq(comando_mysql)
            enviar_comando_a_rabbitmq(comando_mongodb)

            # Crear diccionario con información para el voucher
            reserva_info = {
                'nombre_apellido': nombre_apellido,
                'pais': pais,
                'Numero de Documento': documento,
                'Fecha de Nacimiento': nacimiento,
                'sexo': sexo,
                'email': email,
                'telefono': telefono,
                'ID_Vuelos': vuelo
                # Agrega más información según sea necesario
            }
            print(f'ID_Vuelos en reserva_info: {reserva_info["ID_Vuelos"]}')  # Añade este print

            email_usuario = email
            detalles_reserva = {'nombre_apellido': nombre_apellido, 'pais': pais, 'Numero de Documento': documento, 'Fecha de Nacimiento': nacimiento, 'sexo': sexo, 'email': email, 'telefono': telefono, 'ID_Vuelos': vuelo}
            enviar_correo_reserva(email_usuario, detalles_reserva, reserva_info)
            
            # Redirige al usuario a la vista del voucher
            return generar_voucher(request, reserva_info)
        except Exception as e:
            # Manejar errores (puedes redirigir a una página de error)
            print(f'Error al procesar la reserva: {e}')
    
    return render(request, 'Reserva/reserva.html', {'usuario_rut': usuario_rut})
