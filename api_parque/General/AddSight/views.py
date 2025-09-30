from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import vision

from api_parque.models import Sighting, TypeRegister, Register

from uuid import uuid4
from django.conf import settings
import boto3

from google.cloud import vision
from google.oauth2 import service_account
import json
import os

def get_vision_client():
    """Crea el cliente de Vision solo cuando se necesita"""
    # Intenta obtener las credenciales desde variable de entorno
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS')
    
    if credentials_json:
        # En producción (Render)
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
    else:
        # En desarrollo local
        CREDENTIALS_PATH = r"C:/Users/MarcoVallejo/Downloads/e-caldron-419505-f1d28e04ecc1.json"
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    
    return vision.ImageAnnotatorClient(credentials=credentials)


# Configuración de S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


def upload_to_s3(file, folder):
    if file:
        try:
            file_key = f"{folder}/{uuid4()}_{file.name}"
            s3_client.upload_fileobj(
                Fileobj=file,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_key,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'private'
                }
            )
            return file_key
        except Exception as e:
            print(f"Error al subir archivo: {e}")
            return None
    return None


def analyze_image_safe_search(file_bytes):
    """Valida imagen con Google Cloud Vision SafeSearch"""
    # Crear el cliente AQUÍ, no al inicio del módulo
    client = get_vision_client()
    
    image = vision.Image(content=file_bytes)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Bloqueamos si es "LIKELY" o "VERY_LIKELY" en adulto o violencia
    if safe.adult >= 4 or safe.violence >= 4:
        return False, safe

    return True, safe



class AddSighthingView(APIView):

    def post(self, request):
        full_name = request.data.get('full_name', '')
        date = request.data.get('date', '')
        type_register = request.data.get('type_register', '')
        name_register = request.data.get('name_register', '')
        description = request.data.get('description', '')
        photo_file = request.FILES.get("photo")

        if not full_name or not photo_file:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        # --- 1. Validamos con Vision antes de guardar ---
        is_safe, safe_details = analyze_image_safe_search(photo_file.read())
        photo_file.seek(0)  # rebobinar buffer tras leer

        if not is_safe:
            return Response({
                "status": "rejected",
                "details": {
                    "adult": safe_details.adult,
                    "violence": safe_details.violence,
                    "racy": safe_details.racy
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # --- 2. Subimos a S3 solo si pasa validación ---
        photo_key = upload_to_s3(photo_file, "photos")
        if not photo_key:
            return Response({"error": "Error uploading image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            type_register_obj = TypeRegister.objects.get(id=type_register)
            name_register_obj = Register.objects.get(id=name_register)

            add_sighting = Sighting(
                full_name=full_name,
                date=date,
                type_register=type_register_obj,
                sighting_name=name_register_obj,
                description=description,
                photo=photo_key.split("/")[-1]  # solo el nombre
            )
            add_sighting.save()

            return Response({
                "message": "Sighting created successfully",
                "photo": photo_key.split("/")[-1]
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si hay error en la DB → borrar la foto subida
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=photo_key
            )
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
