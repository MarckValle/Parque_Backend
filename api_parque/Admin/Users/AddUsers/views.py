from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import User, TypeUser
from rest_framework.permissions import IsAuthenticated


class AddUserAPiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request): 

        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        age = request.data.get('age', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        type_user = request.data.get('type_user')

        id_type = TypeUser.objects.get(id=type_user)

        try:
            if id_type:
                user = User(first_name=first_name, 
                            last_name=last_name,
                            age=age,
                            phone=phone,
                            email=email,
                            password=password,
                            type_id=id_type,
                            username=email
                        )
                
                user.set_password(password)
                user.save()
                
                return Response({'message': 'user was created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)