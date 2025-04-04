from collections import Counter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import PageVisit, Register
import re

class AllVisitsAPIView(APIView):
    def get(self, request):
        visits = PageVisit.objects.filter(path='/general_netzahualcoyotl/search_register/')
        
        counter = visits.count()
        return Response({
                "message": "Information retrieved successfully",
                "total_visits": counter,
                # "percentage_change": f"{percentage_change:+.2f}%",  # +8.00% / -5.00%
            }, status=status.HTTP_200_OK)
