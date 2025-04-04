from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from api_parque.Admin.Registers.TypeRegister.serializers import TypeRegisterSerializer

from api_parque.models import TypeRegister

class TypeRegisterAPiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        type_register = request.data.get('type_register', '')

        try:
            if type_register:
                type_register = TypeRegister(type_register=type_register)
                type_register.save()
            return Response({'message': 'Type register was created succesfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        
        try:
            type_register = TypeRegister.objects.all()

            serializer = TypeRegisterSerializer(type_register, many=True)

            return Response(serializer.data , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            