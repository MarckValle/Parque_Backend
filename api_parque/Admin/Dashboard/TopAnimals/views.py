from collections import Counter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import PageVisit, Register
import re

class MostPopularRegistersAPIView(APIView):
    def get(self, request):
        visits = PageVisit.objects.filter(path__startswith='/general_netzahualcoyotl/register_card/')
        
        # Extraer IDs desde los paths
        register_ids = []
        for visit in visits:
            match = re.search(r'/register_card/(\d+)/', visit.path)
            if match:
                register_ids.append(int(match.group(1)))

        counter = Counter(register_ids)

        # Top 10 más visitados
        top_items = counter.most_common(10)
        top_ids = [item[0] for item in top_items]
        total_top_visits = sum([item[1] for item in top_items])

        registers = Register.objects.filter(id__in=top_ids)
        register_map = {reg.id: reg for reg in registers}

        result = []
        for reg_id, visits in top_items:
            reg = register_map.get(reg_id)
            if reg:
                popularity = (visits / total_top_visits) * 100 if total_top_visits > 0 else 0
                result.append({
                    "id": reg.id,
                    "name": reg.name,
                    "visits": visits,
                    "popularity": f"{popularity:.2f}%",  # ej. "18.50%"
                    "photo": reg.photo
                })

        return Response({"top_registers": result}, status=status.HTTP_200_OK)
