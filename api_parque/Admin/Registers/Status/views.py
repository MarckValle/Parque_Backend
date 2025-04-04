from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from api_parque.models import Status as st
from api_parque.Admin.Registers.Status.serializers import StatusSerializer

class StatusAPiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        status_ = request.data.get('status', '')

        if status_:
            try:
                    create_status = st(status=status_)
                    create_status.save()
                    return Response({'message': 'Status was created succesfully'}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request):
        user = request.user

        try:
            stat = st.objects.all()
            serializer = StatusSerializer(stat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except stat.DoesNotExist:
             return Response({'error': 'Status does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete (self, request):
        user = request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a status'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            stat = st.objects.get(id=id)
            stat.delete()

            return Response({'message': 'status register was deleted successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_404_NOT_FOUND)
        
    def put (self, request):
        user = request.user
        id = request.data.get('id', None)
        name = request.data.get('name', '')

        if not id:
            return Response({'message': 'id is required to delete a Status'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            stat_data = st.objects.get(id=id)
            stat_data.status = name
            stat_data.save()

            return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)
        
        except st.DoesNotExist:
            return Response({'error': 'Status not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                 

