from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_parque.models import TypeUser
from api_parque.Admin.Users.UserType.serializers import TypeUserSerializer

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
            
    def get(self, request):

        try:

            type_u = TypeUser.objects.all()
            serializer = TypeUserSerializer(type_u, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        