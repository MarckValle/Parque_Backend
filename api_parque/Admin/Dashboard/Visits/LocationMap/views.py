# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from api_parque.models import PageVisit

class VisitorsSummaryAPIView(APIView):
    def get(self, request):
        # Filtramos solo rutas de general_netzahualcoyotl
        visits = (
            PageVisit.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False,
                path__startswith="/general_netzahualcoyotl/"
            )
            .values('city', 'country', 'latitude', 'longitude')
            .annotate(visits=Count('id'))
            .order_by('-visits')
        )

        return Response(list(visits))
