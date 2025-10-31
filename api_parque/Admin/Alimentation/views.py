from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import Alimentation
from django.conf import settings
import boto3
from api_parque.Admin.Alimentation.TableFeed.serializers import TableFeedSerializer

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


class CreateAlimentationtView(APIView):
    def post(self, request):
        name = request.data.get("name", "")
        photo = upload_to_s3(request.FILES.get("photo"), "photos")

        if not name or not photo:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Guardar solo el nombre del archivo
            alimentation = Alimentation(name=name, photo=photo['key'])
            alimentation.save()

            return Response({"message": "Alimentation created successfully", "file_name": photo['key']}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    def put(self, request):
        alimentation_id = request.data.get("id")
        name = request.data.get("name", "")
        photo = request.FILES.get("photo")  # Puede ser None

        if not alimentation_id:
            return Response({"error": "El ID del registro es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscar registro existente
            alimentation = Alimentation.objects.filter(id=alimentation_id).first()
            if not alimentation:
                return Response({"error": "El registro no existe"}, status=status.HTTP_404_NOT_FOUND)

            # Si se subió una nueva imagen, subir a S3
            if photo:
                uploaded_photo = upload_to_s3(photo, "photos")
                alimentation.photo = uploaded_photo['key']  # Guardar solo el nombre del archivo

            # Actualizar nombre
            alimentation.name = name
            alimentation.save()

            return Response({
                "message": "Registro actualizado correctamente",
                "file_name": alimentation.photo
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    
    def delete(self, request):
        request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a feed'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            feed = Alimentation.objects.get(id=id)
            feed.delete()

            return Response({'message': 'Feed was deleted successfully'}, status=status.HTTP_200_OK)
        
        except Alimentation.DoesNotExist:
            return Response({'error': 'There is no feed in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        request.user

        try:

            feeds = Alimentation.objects.all()
            serializer = TableFeedSerializer(feeds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except feeds.DoesNotExist:
            return Response({'error': 'There is no registers in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
