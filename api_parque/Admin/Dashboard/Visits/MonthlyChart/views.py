from django.db.models import Count
from django.db.models.functions import TruncWeek, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from api_parque.models import PageVisit

class VisitStatsView(APIView):
    def get(self, request):
        # Filtrar solo las URLs del módulo general_netzahualcoyotl
        base_filter = PageVisit.objects.filter(path__icontains="/general_netzahualcoyotl/")

        # Agrupar semanalmente
        weekly_data = (
            base_filter
            .annotate(week=TruncWeek('timestamp'))
            .values('week')
            .annotate(visitas=Count('id'))
            .order_by('week')
        )

        # Agrupar mensualmente
        monthly_data = (
            base_filter
            .annotate(month=TruncMonth('timestamp'))
            .values('month')
            .annotate(visitas=Count('id'))
            .order_by('month')
        )

        return Response({
            "weekly": list(weekly_data),
            "monthly": list(monthly_data)
        })
