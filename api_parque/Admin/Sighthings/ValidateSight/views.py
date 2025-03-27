from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api_parque.models import Sighting

class ValidateSighthingsAPiView(APIView):

    def put(self, request):
        try:
            id_sight = request.data.get('id_sighthing', None)
            validate = request.data.get('validated', bool)

            sighthings = Sighting.objects.get(id=id_sight)
            
            sighthings.validated = validate
            sighthings.save()

            return Response({'message': 'Sighthing validated successfully'})
        
        except Sighting.DoesNotExist:
            return Response({'error': 'This register does not exists'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)