from django.urls import path
from .Users.UserType.views import UserTypeAPiView
from .Users.AddUsers.views import AddUserAPiView
from .Habitat.views import HabitatAPiView
from .Registers.TypeRegister.views import TypeRegisterAPiView
from .Registers.Status.views import StatusAPiView
from .Registers.AddRegisters.views import AddRegistersAPiView
from api_parque.Admin.Registers.GetRegisters.views import GetRegistersAPiView
from api_parque.Admin.Habitat.TableHabitats.views import TableHabitatAPiView
from api_parque.Admin.Registers.Status.TableStatus.views import TableStatusAPiView
urlpatterns = [
    path('user_type/', UserTypeAPiView.as_view(), name='add-type'),
    path('add_users/', AddUserAPiView.as_view(), name='add-users'),
    path('habitat/', HabitatAPiView.as_view(), name='add-habitat'),
    path('type_register/', TypeRegisterAPiView.as_view(), name='add-type-register'),
    path('status/', StatusAPiView.as_view(), name='add-type-register'),
    path('add_register/', AddRegistersAPiView.as_view(), name='add-register'),
    path('get_registers/', GetRegistersAPiView.as_view(), name='get-register'),
    path('table_habitats/', TableHabitatAPiView.as_view(), name='get-table-habitats'),
    path('table_status/', TableStatusAPiView.as_view(), name='get-table-status'),
]
