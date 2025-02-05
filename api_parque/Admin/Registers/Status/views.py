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
                 

