from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from api_parque.models import Habitat
from api_parque.Admin.Habitat.serializers import HabitatSerializer

from django.conf import settings
import boto3
from uuid import uuid4
import os
s3_client = boto3.client(
    "s3",
    # Ya no necesitas endpoint_url para AWS S3 estándar
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=settings.AWS_S3_REGION_NAME,
)

def upload_to_s3(file, folder):
    if file:
        try:
            file_key = f"{folder}/{uuid4()}_{file.name}"
            
            # Subir archivo al bucket
            s3_client.upload_fileobj(
                Fileobj=file,
                Bucket= os.getenv('AWS_STORAGE_BUCKET_NAME'),
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

class HabitatAPiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user
        name = request.data.get("name", "")
        photo = upload_to_s3(request.FILES.get("photo"), "photos")
        
        if not name or not photo:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
           

            # Guardar en la base de datos
            habitat = Habitat(name=name, photo=photo['key'])
            habitat.save()

            return Response({"message": "Habitat created successfully", "photo_url": photo['key']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete (self, request):
        user = request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a habitat'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            habitat = Habitat.objects.get(id=id)
            habitat.delete()

            return Response({'message': 'habitat register was deleted successfully'}, status=status.HTTP_200_OK)
        
        except habitat.DoesNotExist:
            return Response({'error': 'There is no registers in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                 
    def put (self, request):
        user = request.user
        id = request.data.get('id', None)
        name = request.data.get('name', '')
        photo = request.data.get('photo', None)

        if not id:
            return Response({'message': 'id is required to delete a habitat'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            habitat = Habitat.objects.get(id=id)
            habitat.name = name
            habitat.photo = photo
            habitat.save()

            return Response({'message': 'Habitat updated successfully'}, status=status.HTTP_200_OK)
        
        except Habitat.DoesNotExist:
            return Response({'error': 'Habitat not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                 
    def get(self, request):
        request.user

        try:

            habitats = Habitat.objects.all()
            serializer = HabitatSerializer(habitats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except habitats.DoesNotExist:
            return Response({'error': 'There is no registers in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
        
        

