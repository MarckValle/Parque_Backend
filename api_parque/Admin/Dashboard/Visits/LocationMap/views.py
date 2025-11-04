# views.py
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from api_parque.models import PageVisit


class GetVisitorsLocations(APIView):
    def get(self, request, *args, **kwargs):
        logs = PageVisit.objects.all().values('ip_address', 'timestamp')
        locations = []

        for log in logs:
            ip = log['ip_address']

            # Evita consultar IPs locales o vacías
            if not ip or ip.startswith(('127.', '192.', '10.')):
                continue

            try:
                res = requests.get(f"https://ip-api.com/json/{ip}", timeout=5)

                if res.get('status') == 'success':
                    locations.append({
                        'ip': ip,
                        'lat': res.get('lat'),
                        'lon': res.get('lon'),
                        'city': res.get('city', ''),
                        'country': res.get('country', ''),
                        'timestamp': log['timestamp']
                    })
            except Exception as e:
                print(f"Error al obtener ubicación de {ip}: {e}")
        
        return Response(locations)
