from rest_framework import serializers
from api_parque.models import Register, TypeRegister, Status
import boto3
from django.conf import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

class TypeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeRegister
        fields = ["id", "type_register"]  # Devuelve ambos valores

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "status"]  # Devuelve ambos valores


class RegistersSerializer(serializers.ModelSerializer):
    # Serializadores relacionados
    type_id = TypeRegisterSerializer()
    status_id = StatusSerializer()

    # URLs prefirmadas para photo, sound y video
    photo = serializers.SerializerMethodField()
    sound = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Register
        fields = '__all__'  # O lista explícita de campos si prefieres
        

    # Función para generar URL prefirmada
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

    # Obtener URL para sound
    def get_sound(self, obj):
        return self.get_presigned_url(obj.sound, "sounds")

    # Obtener URL para video
    def get_video(self, obj):
        return self.get_presigned_url(obj.video, "videos")

    
