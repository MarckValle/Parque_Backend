from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import Threat
from api_parque.Admin.Threat.ThreatTable.serializers import TableThreatSerializer

class CreateThreatView(APIView):
    def post(self, request):
        request.user
        name = request.data.get('name', "")

        if not name:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            # Guardar en la base de datos
            threat = Threat(name=name)
            threat.save()

            return Response({"message": "threat created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a threat'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            threats = Threat.objects.get(id=id)
            threats.delete()

            return Response({'message': 'Threat was deleted successfully'}, status=status.HTTP_200_OK)
        
        except threats.DoesNotExist:
            return Response({'error': 'There is no Threats in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        request.user
        id = request.data.get('id', None)
        name = request.data.get('name', "")

        if not name:
            return Response({"error": "Name and photo are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            # Guardar en la base de datos
            threat = Threat.objects.get(id=id)
            threat.name = name
            threat.save()

            return Response({"message": "threat created successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        request.user

        try:

            threat = Threat.objects.all()
            serializer = TableThreatSerializer(threat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except threat.DoesNotExist:
            return Response({'error': 'There is no registers in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
