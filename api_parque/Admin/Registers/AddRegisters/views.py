from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_parque.models import (
    Register, TypeRegister, Status as st, Habitat, Threat, Alimentation,
    RegisterHabitat, RegisterThreat, RegisterAlimentation
)
from api_parque.Admin.Registers.AddRegisters.serializers import RegisterSerializer
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

# 4. Actualiza tu vista con la nueva función
class AddRegistersAPiView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            name = request.data.get("name", "")
            scientific_name = request.data.get("scientific_name", "")
            function = request.data.get("function", "")
            description = request.data.get("description", "")
            distribution = request.data.get("distribution", "")
            type_id = request.data.get("type_id", "")
            status_id = request.data.get("status_id", "")

            type_obj = TypeRegister.objects.get(id=type_id)
            status_obj = st.objects.get(id=status_id)

            # Usar la nueva función para subir a AWS S3
            photo = upload_to_s3(request.FILES.get("photo"), "photos")
            video = upload_to_s3(request.FILES.get("video"), "videos")
            sound = upload_to_s3(request.FILES.get("sound"), "sounds")
            # El resto del código permanece igual
            # Crear el registro en la base de datos
            new_register = Register(
                name=name,
                scientific_name=scientific_name,
                function=function,
                description=description,
                distribution=distribution,
                sound=sound['key'],
                photo=photo['key'],
                video=video['key'],
                type_id=type_obj,
                status_id=status_obj,
            )
            new_register.save()
            
            # Manejo de relaciones (sin cambios)
            habitat_ids = request.data.get("habitat_ids", [])
            threat_ids = request.data.get("threat_ids", [])
            alimentation_ids = request.data.get("alimentation_ids", [])

            for habitat_id in habitat_ids:
                habitat = Habitat.objects.get(id=habitat_id)
                RegisterHabitat.objects.create(register=new_register, habitat=habitat)

            for threat_id in threat_ids:
                threat = Threat.objects.get(id=threat_id)
                RegisterThreat.objects.create(register=new_register, threat=threat)

            for alimentation_id in alimentation_ids:
                alimentation = Alimentation.objects.get(id=alimentation_id)
                RegisterAlimentation.objects.create(register=new_register, alimentation=alimentation)

            return Response({"message": "Register created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def put (self, request):
        user = request.user
        id = request.data.get('id', None)
        name = request.data.get('name', '')
        scientific_name = request.data.get('scientific_name', None)
        function = request.data.get('function', '')
        description = request.data.get('description', '')
        distribution = request.data.get('distribution', '')
        type_id = request.data.get('type_id', '')
        status_id = request.data.get('status_id', '')

        
        type_id = TypeRegister.objects.get(id=type_id)
        status_id = st.objects.get(id=status_id)

        if not id:
            return Response({'message': 'id is required to delete a Register'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            register = Register.objects.get(id=id)
            register.name = name
            register.scientific_name = scientific_name
            register.function=function
            register.description=description
            register.distribution=distribution
            register.type_id=type_id
            register.status_id=status_id
            register.save()

            return Response({'message': 'Register updated successfully'}, status=status.HTTP_200_OK)
        
        except Register.DoesNotExist:
            return Response({'error': 'Register not found'}, status=status.HTTP_404_NOT_FOUND)
    
        except TypeRegister.DoesNotExist:
            return Response({'error': 'Register not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except st.DoesNotExist:
            return Response({'error': 'Register not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete (self, request):
        user = request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a register'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            register = Register.objects.get(id=id)
            register.delete()

            return Response({'message': 'register register was deleted successfully'}, status=status.HTTP_200_OK)
        
        except register.DoesNotExist:
            return Response({'error': 'There is no registers in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):

        try:
            registers = Register.objects.all()
            registers = RegisterSerializer(registers, many=True)

            return Response(registers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



