from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_reserva(email, detalles_reserva):
    asunto = 'Confirmación de Reserva de Vuelo'
    mensaje = f'Tu reserva para el vuelo {detalles_reserva.get("Nombre vuelo", "Desconocido")} ha sido confirmada. Detalles: {detalles_reserva}'

    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email])
