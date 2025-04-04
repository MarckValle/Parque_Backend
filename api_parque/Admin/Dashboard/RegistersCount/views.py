from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from api_parque.models import Register

class RegistersCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Conteo total de registros
        count_register = Register.objects.count()

        # Fecha de ayer
        # yesterday = now().date() - timedelta(days=1)

        # Contar registros creados ayer
        # count_yesterday = Register.objects.filter(created_at__date=yesterday).count()

        # # Calcular porcentaje de cambio respecto a ayer
        # if count_yesterday > 0:
        #     percentage_change = ((count_register - count_yesterday) / count_yesterday) * 100
        # else:
        #     percentage_change = 100 if count_register > 0 else 0  # Evita división entre 0

        return Response(
            {
                "message": "Information retrieved successfully",
                "total_registers": count_register,
                # "percentage_change": f"{percentage_change:+.2f}%",  # +8.00% / -5.00%
            },
            status=status.HTTP_200_OK,
        )
