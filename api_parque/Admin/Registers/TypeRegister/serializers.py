from rest_framework import serializers
from api_parque.models import TypeRegister

class TypeRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeRegister
        fields = ['id', 'type_register']