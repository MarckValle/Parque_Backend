from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_parque.models import TypeUser

class UserTypeAPiView(APIView):
    
    def post(self, request):
        type = request.data.get('type', '')

        if type:
            try:
                type_user = TypeUser(type_user=type)    
                type_user.save()
                return Response({'message': 'Add type successfully', 'type': type}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({'message': 'Error'}, status=status.HTTP_404_NOT_FOUND)