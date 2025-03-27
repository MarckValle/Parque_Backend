from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api_parque.models import Comments

class SendCommentView(APIView):

    def post(self, request):
        try:
            full_name = request.data.get('full_name', '')
            email = request.data.get('email', '')
            description = request.data.get('description', '')
            type_comment = request.data.get('type_comment', '')

            if not email and not description:
                return Response({'error': 'Email and description are required'}, status=status.HTTP_403_FORBIDDEN)
            
            add_comment = Comments(
                full_name=full_name,
                email=email, 
                description=description,
                type_comment=type_comment
            )
            add_comment.save()
            return Response({'message': 'Comment added succesfully'}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)