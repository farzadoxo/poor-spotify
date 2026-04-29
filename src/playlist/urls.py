from django.urls import path

import views


urlpatterns = [
    path('all/',views.get_all_playlist),
    path('<int:playlist_id>/',views.get_playlist),
    path('new/',views.new_playlist),
    path('add/<int:playlist_id>/<int:music_id>/')
]