from rest_framework import serializers
from api_parque.models import Habitat

class HabitatSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Habitat
        fields = ['id', 'name', 'photo']