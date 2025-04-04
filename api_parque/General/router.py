from django.urls import path
from api_parque.General.AddSight.views import AddSighthingView
from api_parque.General.SendComments.views import SendCommentView
from api_parque.General.Games.GetPhotos.views import GetPhotosAPIView
from api_parque.General.Games.GuessImage.views import GuessPhotoAPIView
from api_parque.Admin.Registers.RegisterCard.views import RegisterCardAPIView
from api_parque.Admin.CountVisit import views
from api_parque.General.SearchRegisters.views import SearchRegistersAPIView
urlpatterns = [
    path('add_sighthing/' , AddSighthingView.as_view() , name='add_sighthing'),
    path('send_comments/' , SendCommentView.as_view() , name='send_comments'),
    path('get_photos/' , GetPhotosAPIView.as_view() , name='get_photos'),
    path('guess_photo/' , GuessPhotoAPIView.as_view() , name='guess_photo'),
    path('api/stats/', views.VisitStatsView.as_view()),
    path('register_card/<int:register_id>/', RegisterCardAPIView.as_view(), name='get-register-card'),
    path('search_register/', SearchRegistersAPIView.as_view(), name='search-register'),
]
