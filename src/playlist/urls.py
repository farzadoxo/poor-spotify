from django.urls import path
from . import views


urlpatterns = [
    path('all/',views.get_all_playlist),
    path('<int:playlist_id>/',views.get_playlist),
    path('new/<str:playlist_name>/',views.new_playlist),
    path('delete/',views.delete_playlist),
    path('music/add/<int:playlist_id>/<int:music_id>/',views.add_to_playlist),
    path('music/remove/<int:playlist_id>/<int:music_id>/',views.remove_music_from_playlist)
]