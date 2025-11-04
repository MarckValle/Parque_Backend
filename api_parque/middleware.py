import requests
from api_parque.models import PageVisit

class VisitorCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.path.startswith('/admin_netzahualcoyotl'):
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            user = request.user if request.user.is_authenticated else None

            # Crear el registro base
            visit = PageVisit.objects.create(
                path=request.path,
                ip_address=ip,
                user_agent=user_agent,
                user=user
            )

            # Verificar si ya tenemos datos de esa IP
            has_location = PageVisit.objects.filter(ip_address=ip, latitude__isnull=False).exists()

            if not has_location and ip not in ('127.0.0.1', 'localhost'):
                try:
                    res = requests.get(f"http://ip-api.com/json/{ip}").json()
                    if res['status'] == 'success':
                        visit.city = res.get('city')
                        visit.region = res.get('regionName')
                        visit.country = res.get('country')
                        visit.latitude = res.get('lat')
                        visit.longitude = res.get('lon')
                        visit.save()
                except Exception as e:
                    print(f"Error obteniendo datos de IP {ip}: {e}")
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
