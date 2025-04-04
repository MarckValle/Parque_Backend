from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api_parque.Admin.Threat.ThreatTable.serializers import TableThreatSerializer
from api_parque.models import Threat

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = None
    
class TableThreatsAPiView(APIView):
    
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
            request.user
            page_size = request.data.get('page_size', 10)
            try:
                threats = Threat.objects.all()
                paginator = CustomPageNumberPagination()
                paginator.page_size = page_size
                paginated_executions = paginator.paginate_queryset(threats, request)

                # Serializar los datos paginados
                serializer = TableThreatSerializer(paginated_executions, many=True)
                paginated_response_data = serializer.data

                # Add information about the total number of pages and the current page to the response
                paginated_response = paginator.get_paginated_response(paginated_response_data)
                paginated_response.data['total_pages'] = paginator.page.paginator.num_pages
                paginated_response.data['current_page'] = paginator.page.number

                # Append the personal header "row" with the info from the get rows 
                rows_header_value = f"{paginator.page.start_index()}-{paginator.page.end_index()}"
                paginated_response.data['rows'] = rows_header_value

                return paginated_response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)