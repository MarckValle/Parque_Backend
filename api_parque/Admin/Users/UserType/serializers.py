from rest_framework import serializers
from api_parque.models import TypeUser

class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeUser
        fields = ['id', 'type_user']