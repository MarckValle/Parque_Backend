from rest_framework import serializers
from api_parque.models import Register, TypeRegister, Status, Habitat, Threat, Alimentation
import boto3
from django.conf import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

class AlimentationSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField()

    class Meta:
        model = Alimentation
        fields = ["id", "name", "photo"]  # Ajusta los campos según el modelo

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

class TypeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeRegister
        fields = ["id", "type_register"]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "status"]

class HabitatSerializer(serializers.ModelSerializer):

    photo = serializers.SerializerMethodField()

    class Meta:
        model = Habitat
        fields = ["id", "name", "photo", "description"]

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

class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threat
        fields = ["id", "name"]

class RegisterSerializer(serializers.ModelSerializer):
    type_id = TypeRegisterSerializer()  # Relación con TypeRegister
    status_id = StatusSerializer()  # Relación con Status
    habitats = HabitatSerializer(many=True)  # Relación ManyToMany con Habitat
    threats = ThreatSerializer(many=True)  # Relación ManyToMany con Threat
    alimentations = AlimentationSerializer(many=True)
    photo = serializers.SerializerMethodField()
    sound = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Register
        fields = [
            "id", "name", "scientific_name", "function", "description", "habitat",
            "distribution", "sound", "photo", "video", "type_id", "status_id",
            "habitats", "threats", "alimentations"
        ]

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

    

