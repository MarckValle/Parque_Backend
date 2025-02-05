from rest_framework import serializers
from api_parque.models import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Status
        fields = [ 'id', 'status' ]