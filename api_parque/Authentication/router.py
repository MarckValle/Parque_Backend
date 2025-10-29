from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api_parque.Authentication.Me.views import MeAPiView

urlpatterns = [
    path('login/' , jwt_views.TokenObtainPairView.as_view() , name='login'),
    path('login/refresh/' , jwt_views.TokenRefreshView.as_view() ,name='logout'),
    path('api/me/', MeAPiView.as_view() , name='api-me')
]
