from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def enviar_correo_reserva(email, detalles_reserva, reserva_info):
    asunto = 'Confirmación de Reserva de Vuelo'
    
    # Agrega el ID_Vuelos al diccionario de detalles_reserva
    mensaje_html = render_to_string('Historial/confirmacion_reserva_email.html', {
        'detalles_reserva': detalles_reserva,
        'reserva_info': reserva_info,
    })

    mensaje_texto = strip_tags(mensaje_html)

    send_mail(asunto, mensaje_texto, settings.EMAIL_HOST_USER, [email], html_message=mensaje_html)
