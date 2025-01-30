from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_parque.models import Register, TypeRegister, Status as st

class AddRegistersAPiView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        name = request.data.get('name', '')
        scientific_name = request.data.get('scientific_name', '')
        function = request.data.get('function', '')
        description = request.data.get('description', '')
        distribution = request.data.get('distribution', '')
        sound = request.data.get('sound', '')
        photo = request.data.get('photo', '')
        video = request.data.get('video', '')
        type_id = request.data.get('type_id', '')
        status_id = request.data.get('status_id', '')

        type_id = TypeRegister.objects.get(id=type_id)
        status_id = st.objects.get(id=status_id)
        
        if type_id and status_id:
            try:

                new_register = Register(
                    name=name,
                    scientific_name=scientific_name,
                    function=function,
                    description=description,
                    distribution=distribution,
                    sound=sound,
                    photo=photo,
                    video=video,
                    type_id=type_id,
                    status_id=status_id
                )
                new_register.save()
                return Response({'message': 'Register created successfully'}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



