from django.urls import path
from .Users.UserType.views import UserTypeAPiView
from .Users.AddUsers.views import AddUserAPiView
from .Habitat.views import HabitatAPiView
from .Registers.TypeRegister.views import TypeRegisterAPiView
from .Registers.Status.views import StatusAPiView
from .Registers.AddRegisters.views import AddRegistersAPiView

urlpatterns = [
    path('user_type/', UserTypeAPiView.as_view(), name='add-type'),
    path('add_users/', AddUserAPiView.as_view(), name='add-users'),
    path('habitat/', HabitatAPiView.as_view(), name='add-habitat'),
    path('type_register/', TypeRegisterAPiView.as_view(), name='add-type-register'),
    path('status/', StatusAPiView.as_view(), name='add-type-register'),
    path('add_register/', AddRegistersAPiView.as_view(), name='add-register'),
]
