from rest_framework import serializers
from api_parque.models import Threat

class TableThreatSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Threat
        fields = ['id', 'name']
