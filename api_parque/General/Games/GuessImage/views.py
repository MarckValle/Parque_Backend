from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import Register
import boto3
from django.conf import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

def get_presigned_url(file_name, folder):
    """Genera una URL prefirmada si el archivo existe."""
    if file_name:
        try:
            file_key = f"{folder}/{file_name}"  # Ruta en S3
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_key,
                },
                ExpiresIn=604800  # 1 semana en segundos
            )
            return url
        except Exception as e:
            print(f"Error al generar URL: {e}")
            return None
    return None


class GuessPhotoAPIView(APIView):
    def get(self, request):
        try:
            # Creamos una lista de diccionarios con nombre y URL de las fotos
            
            photos_data = [
                {
                    "name": register.name,
                    "photo": get_presigned_url(register.photo, "photos") if register.photo else None
                }
                for register in Register.objects.all()
                if register.photo and register.photo.lower().endswith((".jpg", ".jpeg", ".png"))
            ]

            return Response({"photos": photos_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
