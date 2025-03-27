from rest_framework.views import APIView
import boto3
from rest_framework.response import Response
from rest_framework import status

from api_parque.models import Sighting, TypeRegister, Register

from uuid import uuid4
from django.conf import settings
import boto3

s3_client = boto3.client(
    "s3",
    # Ya no necesitas endpoint_url para AWS S3 estándar
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

def upload_to_s3(file, folder):
    if file:
        try:
            file_key = f"{folder}/{uuid4()}_{file.name}"
            
            # Subir archivo al bucket
            s3_client.upload_fileobj(
                Fileobj=file,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_key,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'private'
                }
            )
            
            # Obtener solo el nombre del archivo
            file_name = file_key.split("/")[-1]

            return {
                'key': file_name  # Guardamos solo el nombre del archivo
            }
        except Exception as e:
            print(f"Error al subir archivo: {e}")
            return None
    return None


class AddSighthingView(APIView):

    def post(self, request):

        full_name = request.data.get('full_name', '')
        date = request.data.get('date', '')
        type_register = request.data.get('type_register', '')
        name_register = request.data.get('name_register', '')
        description = request.data.get('description', '')
        photo = upload_to_s3(request.FILES.get("photo"), "photos")

        if not full_name and not photo:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        type_register = TypeRegister.objects.get(id=type_register)

        name_register = Register.objects.get(id=name_register)

        try:
           

            add_sighting = Sighting(
                full_name=full_name,
                date=date,
                type_register=type_register,
                sighting_name=name_register,
                description=description,
                photo=photo['key']
            )

            add_sighting.save()

            return Response({"message": "sighiting was created successfully", "photo_url": photo['key']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)