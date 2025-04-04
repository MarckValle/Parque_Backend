from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from api_parque.models import Register
from api_parque.General.SearchRegisters.serializers import RegisterSerializer

class SearchRegistersAPIView(APIView):
    def post(self, request):
        try:
            name = request.data.get('name', '')
            type_register = request.data.get('type_register', '')

            query = Q()
            if name:
                query |= Q(name__icontains=name)
            if type_register:
                query |= Q(type_register__icontains=type_register)

            results = Register.objects.filter(query)
            serializer = RegisterSerializer(results, many=True)

            return Response({'results': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
