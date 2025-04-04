from rest_framework import serializers
from api_parque.models import PageVisit

class PageVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageVisit
        fields = '__all__'

class VisitStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()