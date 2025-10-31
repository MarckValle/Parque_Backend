from api_parque.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'El correo no está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generar token y uid
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Enlace de restablecimiento
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        # Enviar correo
        context = {'user': user, 'reset_link': reset_link}
        html_message = render_to_string('ResetPassword.html', context)
        email_message = EmailMessage(
            subject='Recuperación de contraseña',
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.content_subtype = "html"
        email_message.send()

        return Response({'message': 'Correo de recuperación enviado correctamente.'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Enlace inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'El token es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Token válido.', 'uid': uidb64, 'token': token})


class UpdatePasswordView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'message': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)
