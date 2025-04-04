from rest_framework import serializers
from api_parque.models import Register

class RegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Register
        fields = '__all__'