from rest_framework import serializers
from api_parque.models import Register

class RegistersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Register
        fields = ['id', 'name', 'scientific_name', 'function', 'description', 'distribution', 'sound', 'photo', 'video', 'type_id', 'status_id' ]