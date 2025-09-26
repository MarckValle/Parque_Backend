from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api_parque.models import Sighting
from .Serializers import SightingSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = None


class GetSights(APIView):
    def get(self, request):
        try:
            queryset = Sighting.objects.filter(validated=True).order_by("-date")  # 👈 solo validados

            # paginación
            paginator = CustomPageNumberPagination()
            result_page = paginator.paginate_queryset(queryset, request)

            serializer = SightingSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
