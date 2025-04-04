from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from api_parque.models import Sighting
from api_parque.Admin.Sighthings.GetSighthing.serializers import SighthingSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = None

class GetSighthingsView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.user
        page_size = request.data.get('page_size', 10)
        try:
            # Filtrar solo los avistamientos que no están validados
            sighting = Sighting.objects.filter(validated=False)

            paginator = CustomPageNumberPagination()
            paginator.page_size = page_size
            paginated_executions = paginator.paginate_queryset(sighting, request)

            # Serializar los datos paginados
            serializer = SighthingSerializer(paginated_executions, many=True)
            paginated_response_data = serializer.data

            # Agregar información sobre el número total de páginas y la página actual
            paginated_response = paginator.get_paginated_response(paginated_response_data)
            paginated_response.data['total_pages'] = paginator.page.paginator.num_pages
            paginated_response.data['current_page'] = paginator.page.number

            # Agregar información de filas mostradas
            rows_header_value = f"{paginator.page.start_index()}-{paginator.page.end_index()}"
            paginated_response.data['rows'] = rows_header_value

            return paginated_response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
