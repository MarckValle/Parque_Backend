from django.urls import path
from .AddUserType.views import AddUserTypeAPiView
from .AddUsers.views import AddUserAPiView

urlpatterns = [
    path('add_type/', AddUserTypeAPiView.as_view(), name='add-type'),
    path('add_users/', AddUserAPiView.as_view(), name='add-users'),
]
