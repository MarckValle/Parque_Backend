from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from api_parque.models import Habitat

class HabitatAPiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user
        name = request.data.get('name', '')
        photo = request.data.get('photo', '')

        try:
            if name:
                habitat = Habitat(name=name, photo=photo)
                habitat.save()
            return Response({'message': 'Habitat was created succesfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        request.user
        try:
            habitat = Habitat.objects.all()
            habitats = {
                'habitat': habitat.id
            }
            return Response(habitats, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
