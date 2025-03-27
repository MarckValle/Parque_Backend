from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import Register
from api_parque.Admin.Registers.RegisterCard.serializers import RegisterSerializer

class RegisterCardAPIView(APIView):
    def post(self, request):
        register_id = request.data.get("register_id", None)
        
        if not register_id:
            return Response({"error": "El register_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            register = Register.objects.select_related(
                "type_id", "status_id"
            ).prefetch_related(
                "habitats", "threats", "alimentations"  # Incluir prefetch de alimentación
            ).get(id=register_id)

            serializer = RegisterSerializer(register)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Register.DoesNotExist:
            return Response({"error": "Registro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

