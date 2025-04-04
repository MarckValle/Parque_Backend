from rest_framework import serializers
from api_parque.models import Alimentation
import boto3
from django.conf import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


class TableFeedSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    class Meta: 
        model = Alimentation
        fields = '__all__'

    def get_presigned_url(self, file_name, folder):
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

    # Obtener URL para photo
    def get_photo(self, obj):
        return self.get_presigned_url(obj.photo, "photos")
