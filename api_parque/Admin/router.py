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
from api_parque.Admin.Users.TableUsers.views import TableUserAPiView

from api_parque.Admin.Sighthings.GetSighthing.views import GetSighthingsView
from api_parque.Admin.Sighthings.ValidateSight.views import ValidateSighthingsAPiView
from api_parque.Admin.Alimentation.views import CreateAlimentationtView
from api_parque.Admin.Threat.views import CreateThreatView
from api_parque.Admin.Threat.ThreatTable.views import TableThreatsAPiView
from api_parque.Admin.Alimentation.TableFeed.views import TableFeedAPiView

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
    path('table_users/', TableUserAPiView.as_view(), name='get-table-users'),
    
    path('get_all_sighthings/', GetSighthingsView.as_view(), name='get-sighthing-card'),
    path('validate_sighthings/', ValidateSighthingsAPiView.as_view(), name='validate-sighthing-card'),
    path('create_feed/', CreateAlimentationtView.as_view(), name='create-feed'),
    path('create_threat/', CreateThreatView.as_view(), name='create-threat'),
    path('table_threat/', TableThreatsAPiView.as_view(), name='table-threat'),
    path('table_feed/', TableFeedAPiView.as_view(), name='table-feed'),
   
]
