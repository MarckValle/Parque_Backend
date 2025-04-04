from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import viewsets, views
from rest_framework.response import Response
from api_parque.models import PageVisit
from .serializers import PageVisitSerializer, VisitStatsSerializer
from django.utils import timezone


class PageVisitViewSet(viewsets.ModelViewSet):
    queryset = PageVisit.objects.all()
    serializer_class = PageVisitSerializer

class VisitStatsView(views.APIView):
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        
        # Agrupar por día y contar visitas
        stats = PageVisit.objects.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(days=days)
        ).annotate(
            date=TruncDate('timestamp')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        serializer = VisitStatsSerializer(stats, many=True)
        return Response(serializer.data)
