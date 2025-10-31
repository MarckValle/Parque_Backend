from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api_parque.Authentication.Me.views import MeAPiView
from api_parque.Authentication.ResetPassword import views
urlpatterns = [
    path('login/' , jwt_views.TokenObtainPairView.as_view() , name='login'),
    path('login/refresh/' , jwt_views.TokenRefreshView.as_view() ,name='logout'),
    path('api/me/', MeAPiView.as_view() , name='api-me'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('update-password/', views.UpdatePasswordView.as_view(), name='update_password'),
]
